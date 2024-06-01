FROM apache/superset:latest

USER root

RUN <<EOF
    pip install trino

    apt update
    apt install -y jq
EOF

USER superset