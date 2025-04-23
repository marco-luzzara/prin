ARG SUPERSET_VERSION
FROM apache/superset:${SUPERSET_VERSION}

USER root

RUN <<EOF
    pip install trino

    apt update
    apt install -y jq
EOF

ENV ADMIN_USERNAME=admin
ENV ADMIN_PASSWORD=admin
ENV ADMIN_EMAIL=

USER superset