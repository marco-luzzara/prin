#!/bin/bash

END_TIMESTAMP=0
while :
do 
    START_TIMESTAMP="$END_TIMESTAMP"
    END_TIMESTAMP="$EPOCHSECONDS"

    echo "$(date) - Starting CDC with interval [$START_TIMESTAMP, $END_TIMESTAMP[ ..."

    ./trino --server "$TRINO_ENDPOINT" --user trino --execute "
        INSERT INTO hive.default.patient_records (id, luogo_di_nascita, patologia, created_at)
        SELECT kafka_key, luogo_di_nascita, patologia, _timestamp 
        FROM kafka.filesystemwatcher.\"medical-records\"
        WHERE _timestamp >= from_unixtime($START_TIMESTAMP) AND _timestamp < from_unixtime($END_TIMESTAMP);
    " && echo "CDC Completed successfully" || echo "CDC process failed"

    sleep "$FLUSH_DELAY_SECONDS"
done
