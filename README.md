# PRIN

## Sources

- [How to (actually) Configure a Kafka Cluster in KRaft Mode For Testing & Development](https://medium.com/@hjdjoo/how-to-actually-configure-a-kafka-cluster-in-kraft-mode-for-testing-development-8f90f09e36b1)
- [The Apache Kafka Control Plane](https://developer.confluent.io/courses/architecture/control-plane/)

## Run

First run the compose file:

```bash
set -a
source .env
set +a
docker compose up -d
```

To run different configurations of the docker compose, you can set profiles:

```bash
docker compose --profile ranger-test -f docker-compose.yml -f docker-compose-profiles.yml up -d
```

Similarly, you can limit the resources of any container by including the `docker-compose-resource-limits.yml`.

The `watcher` service monitors the `./remote_machine/to-watch` folder for any new Excel file. Valid extensions are `.xls`, `.xlsx`, `.ods`. When a new Excel is detected, an event with the patient information are sent to the topic `filesystemwatcher.medical-records`. These events can be queried from Trino thanks to the Kafka connector for Trino. To run any query:

```bash
docker compose exec -it trino bash
# on the trino shell then run...
trino --catalog kafka --schema filesystemwatcher
```
```sql
-- on the trino cli you can select all the records
SELECT * FROM "medical-records";
```

---

## Produce Test Data with Kafka

To produce test data with Kafka, run:

```bash
docker exec -it prin-kafka-broker-0-1 bash
kafka-console-producer.sh \
    --topic filesystemwatcher.test \ # specify a previously created topic
    --property parse.key=true \
    --property key.separator="|" \
    --broker-list localhost:9092 #,kafka-broker-1:9092
1|{"prop1":"test", "prop2": 10}
```

---

## Insert on S3

To test the insertion on S3, create a table from Trino:

```bash
trino --catalog hive --schema default
```

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