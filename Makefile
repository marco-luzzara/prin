SHELL = /bin/bash

COMPOSE_PROFILES ?= *
STANDARD_COMPOSE_FILES = docker-compose.yml docker-compose-profiles.yml
ADDITIONAL_COMPOSE_FILES ?= 
COMPOSE_FILES_OPTIONS = $(foreach cf,$(STANDARD_COMPOSE_FILES) $(ADDITIONAL_COMPOSE_FILES), -f $(cf))

.PHONY: init up down

init:
	mkdir -p kafka/data0 minio/data solr postgres/data
	chmod 777 solr

up: init
	set -a && \
	source .env && \
	set +a && \
	COMPOSE_PROFILES=${COMPOSE_PROFILES} docker compose $(COMPOSE_FILES_OPTIONS) up -d

down:
	docker compose down -v