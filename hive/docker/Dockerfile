ARG HIVE_VERSION
FROM apache/hive:${HIVE_VERSION}

USER root

ARG ATLAS_VERSION=2.3.0

COPY apache-atlas-${ATLAS_VERSION}-hive-hook.tar.gz /tmp/atlas-hook/

RUN <<EOF
    apt update
    apt install -y wget tar

    # install driver
    cd lib
    wget https://jdbc.postgresql.org/download/postgresql-42.7.5.jar
    cd ..

    # enable hadoop-aws jars
    ln -s /opt/hadoop/share/hadoop/tools/lib/hadoop-aws* /opt/hadoop/share/hadoop/common/lib/
    ln -s /opt/hadoop/share/hadoop/tools/lib/aws-java-sdk* /opt/hadoop/share/hadoop/common/lib/

    # install hive hook for atlas
    mkdir -p atlas/hook/hive
    cd /tmp/atlas-hook
    tar -xf ./apache-atlas-${ATLAS_VERSION}-hive-hook.tar.gz
    cd $HIVE_HOME
    cp -a /tmp/atlas-hook/apache-atlas-hive-hook-${ATLAS_VERSION}/hook/hive/. atlas/hook/hive
    rm -r /tmp/atlas-hook
EOF

USER hive
