ARG HIVE_VERSION
FROM apache/hive:${HIVE_VERSION}

USER root

RUN <<EOF
    apt update
    apt install -y wget
    cd lib
    wget https://jdbc.postgresql.org/download/postgresql-42.7.5.jar

    ln -s /opt/hadoop/share/hadoop/tools/lib/hadoop-aws* /opt/hadoop/share/hadoop/common/lib/
    ln -s /opt/hadoop/share/hadoop/tools/lib/aws-java-sdk* /opt/hadoop/share/hadoop/common/lib/
EOF

USER hive
