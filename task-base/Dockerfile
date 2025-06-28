# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install pip-tools


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


FROM base AS example-prod

RUN pip install build

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=task-api-utils/requirements.in,target=/custom-libs/task-api-utils/requirements.in \
    cd /custom-libs/task-api-utils && pip-compile requirements.in && pip-sync

COPY ./task-api-utils /custom-libs/task-api-utils

RUN <<EOF
    python -m build /custom-libs/task-api-utils
    pip install /custom-libs/task-api-utils
EOF

WORKDIR /example

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=example/requirements.in,target=/example/requirements.in \
    pip-compile requirements.in && pip-sync

COPY ./example .

ENV TRINO_USER=trino
ENV TRINO_GROUP=
ENV TRINO_ENDPOINT=trino:8080
ENV TRINO_CATALOG=hive
ENV TRINO_SCHEMA=default
ENV TASK_SCOPE=
ENV TASK_APIS_BASE_URL=http://task-apis

CMD ["python", "main.py"]


