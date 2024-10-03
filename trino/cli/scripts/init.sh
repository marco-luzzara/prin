#!/bin/bash

precondition_satisfied=false
while ! $precondition_satisfied
do
    echo "Testing precondition: 'hive' catalog accessible ..."
    ./trino --server "$TRINO_ENDPOINT" --catalog hive --schema default --user trino --execute "SHOW TABLES;" && \
        { echo "'hive' is now accessible" && precondition_satisfied=true ; } || \
        precondition_satisfied=false
done

INIT_SQL_SCRIPT="
    CREATE TABLE IF NOT EXISTS patient_records (
        id BIGINT,
        data_di_nascita DATE,
        luogo_di_nascita VARCHAR,
        age INTEGER,
        sex VARCHAR,
        telefono VARCHAR,
        destrimane_mancino VARCHAR,
        egfr INTEGER,
        prima_visita DATE,
        data_diagnosi DATE,
        patologia VARCHAR,
        a VARCHAR,
        t VARCHAR,
        n VARCHAR,
        created_at TIMESTAMP
    )
    WITH (
        format = 'PARQUET'
    );
"

echo "Creating the patient_records table..."
./trino --server "$TRINO_ENDPOINT" --catalog hive --schema default --user trino --execute "$INIT_SQL_SCRIPT" && \
    echo "patient_records table created"