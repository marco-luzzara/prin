#!/bin/bash

END_TIMESTAMP=0
while :
do 
    START_TIMESTAMP="$END_TIMESTAMP"
    END_TIMESTAMP="$EPOCHSECONDS"

    echo "$(date) - Starting CDC with interval [$START_TIMESTAMP, $END_TIMESTAMP[ ..."

    ./trino --server "$TRINO_ENDPOINT" --user trino --execute "
        INSERT INTO hive.default.patient_records (id, data_di_nascita, luogo_di_nascita, age, sex, telefono,
            destrimane_mancino, egfr, prima_visita, data_diagnosi, patologia, a, t, n, created_at)
        SELECT kafka_key, data_di_nascita, luogo_di_nascita, age, sex, telefono,
            destrimane_mancino, egfr, prima_visita, data_diagnosi, patologia, a, t, n, _timestamp 
        FROM kafka.devprin.\"medical-records\"
        WHERE _timestamp >= from_unixtime($START_TIMESTAMP) AND _timestamp < from_unixtime($END_TIMESTAMP);
    " && echo "CDC Completed successfully" || echo "CDC process failed"

    sleep "$FLUSH_DELAY_SECONDS"
done
