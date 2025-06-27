# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install pip-sync build

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=prin-task-api-utils/requirements.in,target=prin-task-api-utils/requirements.in \
    pip-compile requirements.in && pip-sync

COPY ./prin-task-api-utils ./prin-task-api-utils

RUN pip install ./prin-task-api-utils

ENV TRINO_USER=trino
ENV TRINO_GROUP=
ENV TRINO_ENDPOINT=trino:8080
ENV TRINO_CATALOG=hive
ENV TRINO_SCHEMA=default
ENV TASK_SCOPE=
ENV TASK_APIS_BASE_URL=http://task-apis

CMD ["python", "main.py"]

# DevContainer
# See https://stackoverflow.com/q/68937464/5587393

FROM base AS devcontainer

ARG REMOTE_USER
ARG REMOTE_UID
ARG REMOTE_GID
RUN <<EOF
    addgroup --gid ${REMOTE_GID} ${REMOTE_USER}
    adduser --disabled-password --uid ${REMOTE_UID} --gid ${REMOTE_GID} ${REMOTE_USER}
EOF

ENV HOME=/home/${REMOTE_USER}

USER ${REMOTE_USER}
