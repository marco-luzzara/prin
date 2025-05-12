SHELL = /bin/bash

ENV_FILE ?= .env
COMPOSE_PROFILES ?= *
STANDARD_COMPOSE_FILES = docker-compose.yml docker-compose-profiles.yml
ADDITIONAL_COMPOSE_FILES ?= 
COMPOSE_FILES_OPTIONS = $(foreach cf,$(STANDARD_COMPOSE_FILES) $(ADDITIONAL_COMPOSE_FILES), -f $(cf))

.PHONY: init up down clean-all

# Parameters: \
- ENV_FILE: path of env file containing configuration properties (Default: .env)
init:
	mkdir -p kafka/data0 minio/data solr/data postgres/data atlas/data atlas/logs trino/docker/cdc/data superset/data
	chmod 777 solr/data

	test -e ${ENV_FILE} || { echo "${ENV_FILE} file does not exist" ; exit 1; }

	# trino
	test -e trino/docker/server/rootCA.crt || { echo "rootCA.crt file does not exist. First create it with \`cd trino && make create-crt\`" ; exit 1; }
	test -d trino/docker/server/trino-anonymization-udfs-1.0 || { echo "trino-anonymization-udfs-1.0 directory does not exist. First create it with \`cd trino && make create-udf-package\`" ; exit 1; }

# Parameters: \
- ENV_FILE: path of env file containing configuration properties (Default: .env)\
- COMPOSE_PROFILES: compose profile to activate (Default: *) \
- ADDITIONAL_COMPOSE_FILES: (optional) path to additional compose files
print-rendered:
	set -a && \
	source ${ENV_FILE} && \
	set +a && \
	COMPOSE_PROFILES=${COMPOSE_PROFILES} docker compose $(COMPOSE_FILES_OPTIONS) config

# Parameters: \
- ENV_FILE: path of env file containing configuration properties (Default: .env)\
- COMPOSE_PROFILES: compose profile to activate (Default: *) \
- ADDITIONAL_COMPOSE_FILES: (optional) path to additional compose files \
- SERVICES: (optional) services for which the docker compose action must be applied
up: init
	set -a && \
	source ${ENV_FILE} && \
	set +a && \
	{ test -f hive/.hive_initialized && export SKIP_HIVE_SCHEMA_INIT=true || echo "Hive will initialize the schema..."; } && \
	COMPOSE_PROFILES=${COMPOSE_PROFILES} docker compose $(COMPOSE_FILES_OPTIONS) up -d --build ${SERVICES}
	touch hive/.hive_initialized

# Parameters: \
- SERVICES: (optional) services for which the docker compose action must be applied
down:
	docker compose down -v ${SERVICES}

clean-all: down
	sudo rm -rf kafka/data0 minio/data solr/data/ postgres/data/ atlas/data/ atlas/logs/ trino/docker/cdc/data superset/data
	sudo rm -f hive/.hive_initialized
