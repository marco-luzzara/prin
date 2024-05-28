FROM openjdk:11.0.14-jdk

WORKDIR /cdc

RUN <<EOF
    apt update

    # Cron
    # apt install -y cron
    # (crontab -l 2> /dev/null && echo "* * * * * ./your_script.sh") | crontab -

    # Trino CLI
    curl --output trino https://repo1.maven.org/maven2/io/trino/trino-cli/377/trino-cli-377-executable.jar
    chmod +x trino
    apt install -y less

    # Kafka CLI
    # curl --output kafka.tgz https://downloads.apache.org/kafka/3.6.2/kafka_2.13-3.6.2.tgz
    # tar -xzf kafka.tgz
    # mkdir -p kafka-cli
    # cp kafka/bin/kafka-* kafka-cli/
    # rm -r kafka
EOF

# COPY --chmod=0777 . .

ENV TRINO_ENDPOINT="http://trino:8080"
# ENV PATH="${PATH}:/cdc/kafka-cli"
# ENV KAFKA_BOOTSTRAP_SERVERS="kafka-broker-0:9092"
ENV FLUSH_DELAY_SECONDS=15

ENTRYPOINT ["bash", "-c", "./scripts/init.sh && ./scripts/cdc.sh"]