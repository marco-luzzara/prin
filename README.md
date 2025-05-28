# PRIN

## Sources

- [How to (actually) Configure a Kafka Cluster in KRaft Mode For Testing & Development](https://medium.com/@hjdjoo/how-to-actually-configure-a-kafka-cluster-in-kraft-mode-for-testing-development-8f90f09e36b1)
- [The Apache Kafka Control Plane](https://developer.confluent.io/courses/architecture/control-plane/)

## Run

Modify the `.env` file with the credentials and global configs:

```ini
HIVE_METASTORE_DATABASE_USER=hive_metastore
HIVE_METASTORE_DATABASE_PASSWORD=hive-password

MINIO_ROOT_USER=miniouser
MINIO_ROOT_PASSWORD=miniopassword

SUPERSET_ADMIN_USERNAME=admin
SUPERSET_ADMIN_PASSWORD=admin

RANGER_VERSION=2.6.0
TRINO_VERSION=471

# EXPOSED PORTS
DATA_LOADING_WEBAPP_PORT=5000
MINIO_PORT=9001
TRINO_PORT=8081
HUE_PORT=8888
SUPERSET_PORT=7890
RANGER_PORT=6080
ATLAS_PORT=21000
```

**Note:** if you want to change a credential, search (and replace) it in the entire repo because, for example, the `HIVE_METASTORE_DATABASE_PASSWORD` is created in the `postgres/init/hive-metastore-init.sql` script. 

Create the infrastructure with:

```bash
make up
```

To set profiles:

```bash
make up COMPOSE_PROFILES=without-visualization
```

If `COMPOSE_PROFILES` is unset, then it defaults to `*` (all profiles are activated).

Similarly, you can limit the resources of any container by including the `docker-compose-resource-limits.yml`. To enable the development mode, run:

```bash
make up SERVICES=data-loading-webapp IS_DEV=true
```

The `data-loading-webapp` service exposes a dashboard for uploading patients and MiR results at `/data-loading/patients` and `/data-loading/mir-results`, respectively. Valid extensions for uploaded files are `.xls`, `.xlsx`, `.ods`. When a new Excel is uplaoded, an event with the collected data are sent to the topic `devprin.patients`/`devprin.mir-results`. These events can be queried from Trino thanks to the Kafka connector for Trino. To run any query:

```bash
docker compose exec -it trino bash
# on the trino shell then run...
trino --server https://localhost:8443 --catalog kafka --schema devprin --user test_user1 --password
```
```sql
-- on the trino cli you can select all the records
SELECT * FROM "medical-records";
```

---

## Produce and Consume Test Data with Kafka

To produce test data with Kafka:

```bash
docker compose exec -it kafka-broker-0 bash
kafka-console-producer.sh \
    --topic devprin.test \ # specify a previously created topic
    --property parse.key=true \
    --property key.separator="|" \
    --broker-list localhost:9092 #,kafka-broker-1:9092
1|{"prop1":"test", "prop2": 10}
```

To consume data with Kafka:

```bash
docker compose exec -it kafka-broker-0 bash
kafka-console-consumer.sh \
    --topic devprin.medical-records \
    # --property print.key=true \ you cannot deserialize the key because it is a byte object
    --property key.separator="-" \
    --bootstrap-server localhost:9092 
```

---

## Querying with Trino

First enable authentication (see the properties in the config.properties file). Authentication requires TLS, but you can bypass it by setting:

```
http-server.authentication.allow-insecure-over-http=true
```

By the way, in the demo, HTTPS is used. Now you can authenticate to the server using a different user (`test_user1`), which must be stored in the `password.db` file. 

```bash
trino --server https://localhost:8443 --user test_user1 --password
```

Insert the password and run a simple query. It will return an error: 

> Access Denied: Principal test_user1 cannot become user test_user1

We have not added the user to Ranger yet. So, create a new Ranger User called `test_user1` and modify the Trino policies:

- add to `test_user1` the `impersonate` permission for resource `Trino user: *`
- add to `test_user1` all permissions for resources:
    - Trino catalog: *
    - Trino schema: *
    - Trino table: *
    - Trino column: *
- add to `test_user1` the `execute` permission for resource `Query ID: *`

In the dev deployment, these policies are already present and are called `all - trinouser`, `all - catalog, schema, table, column`, and `all - queryid`.

---

## Insert on S3

To test the insertion on S3, create a table from Trino:

```bash
trino --catalog hive --schema default

# sql query to check the cdc
SELECT * FROM patient_records;
```

To create a new Table use the following commands:

```sql
# query
CREATE TABLE example (
    id INT,
    name VARCHAR
)
WITH (
    format = 'PARQUET'
);

INSERT INTO example
VALUES 
    (1, 'Name1'),
    (2, 'Name2');

SELECT * FROM example;
```

You can get the objects from minio with:

```bash
mc get /data/prin/metadata/example/${object_name}
```

---

## CDC

Kafka is a pub/sub system that could store events indefinetely, but with Trino we cannot perform SQL INSERTs into kafka queues. That is why we need to store them on S3 too, and leverage the Trino integration with Ranger to possibly anonimize the stored data. We are using the Hive metastore to tell Trino where to keep the schema of S3 tables and the format they should have (Parquet). Then, there is a CDC script that periodically copies the Kafka events sent after start time and before the current time (`trino/cli/cdc.sh`) into S3, in a table called `hive.default.patient_records`.

The "flush" delay is determined by the env variable `FLUSH_DELAY_SECONDS` (default 15 seconds)

---

## Hive

Hive runs the schema initialization script every time it starts, unless the env variable `IS_RESUME=true`. However, initializing the schema after it has been previously initialized causes the container failure (only in version 3.1.3, from 4.x this is not an issue, but we need 3.x for Atlas compatibility). This variable is set in the docker compose only when the `hive/.hive_initialized` file exists. This file:
- is created/updated after a `docker compose up`
- is deleted after running `make clean-all`. If you do not need a complete clean, do not execute it.

It might happen that the schema initialization step fails during the Metastore startup. Even if it depends on the `ranger-db` service health, it unexpectedly throws with a failure connection error. Just restart the `hive-metastore` container and should work.

---

## Atlas

To import Hive columns in Atlas:

```bash
docker compose exec -it --user root hive-metastore bash
./import-hive.sh

# Username: admin
# Password: admin

```

Then exit from the container and run the atlas initialization script:

```bash
./atlas/initialize.sh --endpoint http://localhost:21000 --credentials "admin:admin"
```

---

## Ranger

Initialize ranger with:

```bash
./ranger/initialize.sh --endpoint http://localhost:6080 --credentials "admin:rangerR0cks!"
```

Then restart superset:

```bash
docker compose restart superset
```

---

## Issues

### Cannot retrieve Metadata from Ranger

- possibly caused by the exceptions in /var/log/ranger/ranger_admin_sql.log