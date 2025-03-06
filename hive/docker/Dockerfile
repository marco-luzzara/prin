ARG HIVE_VERSION
FROM apache/hive:${HIVE_VERSION}

RUN <<EOF
    apt update
    apt install -y wget
    cd lib
    wget https://jdbc.postgresql.org/download/postgresql-42.7.5.jar
EOF