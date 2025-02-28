SHELL = /bin/bash

ENV_FILE ?= .env
COMPOSE_PROFILES ?= *
STANDARD_COMPOSE_FILES = docker-compose.yml docker-compose-profiles.yml
ADDITIONAL_COMPOSE_FILES ?= 
COMPOSE_FILES_OPTIONS = $(foreach cf,$(STANDARD_COMPOSE_FILES) $(ADDITIONAL_COMPOSE_FILES), -f $(cf))

.PHONY: init up down

init:
	mkdir -p kafka/data0 minio/data solr/data postgres/data
	chmod 777 solr/data

	test -e ${ENV_FILE} || { echo "${ENV_FILE} file does not exist" ; exit 1; }

	# trino
	test -e trino/docker/server/rootCA.crt || { echo "rootCA.crt file does not exist. First create it with \`cd trino && make create-trino-crt\`" ; exit 1; }
	test -d trino/docker/server/trino-anonymization-udfs-1.0 || { echo "trino-anonymization-udfs-1.0 directory does not exist. First create it with \`cd trino && make create-udf-package\`" ; exit 1; }

up: init
	set -a && \
	source ${ENV_FILE} && \
	set +a && \
	COMPOSE_PROFILES=${COMPOSE_PROFILES} docker compose $(COMPOSE_FILES_OPTIONS) up -d

down:
	docker compose down -v
