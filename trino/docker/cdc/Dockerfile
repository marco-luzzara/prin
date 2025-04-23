FROM openjdk:11.0.14-jdk

ARG TRINO_VERSION

WORKDIR /cdc

RUN <<EOF
    apt update

    # Trino CLI
    curl --output trino https://repo1.maven.org/maven2/io/trino/trino-cli/${TRINO_VERSION}/trino-cli-${TRINO_VERSION}-executable.jar
    chmod +x trino
    apt install -y less
EOF

ENV TRINO_ENDPOINT="http://trino:8080"
ENV FLUSH_DELAY_SECONDS=15

VOLUME /cdc/data

ENTRYPOINT ["bash", "-c", "./scripts/init.sh && ./scripts/cdc.sh"]