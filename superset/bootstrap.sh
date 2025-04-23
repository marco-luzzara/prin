#!/bin/bash

# add admin user
superset fab create-admin \
    --username "$ADMIN_USERNAME" \
    --firstname Superset \
    --lastname Admin \
    --email "$ADMIN_EMAIL" \
    --password "$ADMIN_PASSWORD"

superset db upgrade

superset init

/usr/bin/run-server.sh &

# wait until the healthcheck is satisfied
SUPERSET_PORT=${SUPERSET_PORT:-8088}
HEALTH_URL="http://localhost:${SUPERSET_PORT}/health"

while ! curl -f "$HEALTH_URL" > /dev/null 2>&1; do
    echo "Waiting for Superset to become healthy..."
    sleep 5
done

# add trino database 
# see APIs https://superset.apache.org/docs/api/
ACCESS_TOKEN="$(curl "http://localhost:${SUPERSET_PORT}/api/v1/security/login" -X POST -H 'Content-Type: application/json' --data-raw "{
    \"password\": \"$ADMIN_PASSWORD\",
    \"provider\": \"db\",
    \"refresh\": true,
    \"username\": \"$ADMIN_USERNAME\"
}" 2> /dev/null | jq -rc '.access_token')"

CSRF_TOKEN="$(curl -X GET "http://localhost:${SUPERSET_PORT}/api/v1/security/csrf_token/" -H "Content-Type: application/json" \
    --cookie-jar superset/csrf_cookies.txt \
    -H "Authorization: Bearer $ACCESS_TOKEN" 2> /dev/null | jq -rc '.result')"

curl "http://localhost:${SUPERSET_PORT}/api/v1/database/" -X POST -H 'Content-Type: application/json' \
    --cookie superset/csrf_cookies.txt \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "X-CSRFToken: $CSRF_TOKEN" \
    --data-raw '{
    "database_name": "Trino",
    "engine": "trino",
    "configuration_method": "sqlalchemy_form",
    "engine_information": {
        "disable_ssh_tunneling": false,
        "supports_file_upload": true
    },
    "sqlalchemy_uri_placeholder": "engine+driver://user:password@host:port/dbname[?key=value&key=value...]",
    "extra": "{\"allows_virtual_table_explore\":true}",
    "expose_in_sqllab": true,
    "sqlalchemy_uri": "trino://trino@trino:8080/hive"
}'

rm superset/csrf_cookies.txt

sleep inf