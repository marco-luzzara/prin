export RANGER_VERSION=2.5.0
export TRINO_VERSION=451

COMPOSE_PROFILES ?= *

.PHONY: up down

up:
	COMPOSE_PROFILES=${COMPOSE_PROFILES} docker compose -f docker-compose.yml -f docker-compose-profiles.yml up -d

down:
	COMPOSE_PROFILES=${COMPOSE_PROFILES} docker compose -f docker-compose.yml -f docker-compose-profiles.yml down