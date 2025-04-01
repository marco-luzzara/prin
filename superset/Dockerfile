ARG SUPERSET_VERSION
FROM apache/superset:${SUPERSET_VERSION}

USER root

RUN <<EOF
    pip install trino

    # apt update
    # apt install -y jq
EOF

USER superset