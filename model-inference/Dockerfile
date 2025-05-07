ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

COPY . .

ENV TRINO_USER=trino
ENV TRINO_ENDPOINT=trino:8080
ENV TRINO_CATALOG=hive
ENV TRINO_SCHEMA=default

CMD ["sleep", "inf"]