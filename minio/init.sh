#!/bin/bash

mc alias set local_minio http://minio:9000 ${MINIO_ROOT_USER} ${MINIO_ROOT_PASSWORD}
mc mb --ignore-existing local_minio/${MINIO_BUCKET}