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
    CREATE TABLE patient_records (
        id INT,
        luogo_di_nascita VARCHAR,
        patologia VARCHAR,
        created_at TIMESTAMP
    )
    WITH (
        format = 'PARQUET'
    );
"

echo "Creating the patient_records table..."
./trino --server "$TRINO_ENDPOINT" --catalog hive --schema default --user trino --execute "$INIT_SQL_SCRIPT" && \
    echo "patient_records table created"