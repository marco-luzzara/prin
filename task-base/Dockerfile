ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install pip-tools

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.in,target=requirements.in \
    pip-compile requirements.in && pip-sync

COPY . .

ENV TRINO_USER=trino
ENV TRINO_ENDPOINT=trino:8080
ENV TRINO_CATALOG=hive
ENV TRINO_SCHEMA=default

CMD ["python", "main.py"]