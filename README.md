# PRIN

## Sources

- [How to (actually) Configure a Kafka Cluster in KRaft Mode For Testing & Development](https://medium.com/@hjdjoo/how-to-actually-configure-a-kafka-cluster-in-kraft-mode-for-testing-development-8f90f09e36b1)
- [The Apache Kafka Control Plane](https://developer.confluent.io/courses/architecture/control-plane/)

## Run

First run the compose file:

```
docker compose up -d
```

The `watcher` service monitors the `./remote_machine/to-watch` folder for any new Excel file. Valid extensions are `.xls`, `.xlsx`, `.ods`. When a new Excel is detected, an event with the patient information are sent to the topic `filesystemwatcher.medical-records`. These events can be queried from Trino thanks to the Kafka connector for Trino. To run any query:

```
docker exec -it prin-trino-1 bash
# on the trino shell then run...
trino --catalog kafka --schema filesystemwatcher
# on the trino cli then run...
SELECT * FROM "medical-records";
# you should see all the events
```