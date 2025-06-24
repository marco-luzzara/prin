#!/bin/bash

# https://stackoverflow.com/a/78009946/5587393
THIS_CONTAINER_ID="$(cat /proc/self/mountinfo | grep -m1 -oE 'docker/containers/([a-f0-9]+)/' |\
    xargs basename)"

# the spawned containers must be attached to the same network as this container
# because it needs to reach trino (or any other service in the same Docker compose network)
THIS_CONTAINER_NETWORK="$(curl -s --unix-socket /var/run/docker.sock -X GET \
    "http://localhost/containers/$THIS_CONTAINER_ID/json" | \
    jq -r '.NetworkSettings.Networks | keys | .[0]')"

function log_with_date {
    local msg="$1"
    echo "$(date -u +"%Y-%m-%dT%H:%M:%S") - $msg"
}

function start_container {
    local msg="$1"
    local trinoUser="$(echo "$msg" | jq -r '.user')"
    local trinoGroup="$(echo "$msg" | jq -r '.group')"
    local taskEntrypoint="$(echo "$msg" | jq -r '.params.entrypoint')"
    local scope="$(echo "$msg" | jq -r '.scope')"

    log_with_date "Task started by user:group $trinoUser:$trinoGroup"

    local spawnedContainerConfig="$(cat <<JSON
{
    "Image": "$TASK_DOCKER_IMAGE",
    "Entrypoint": $taskEntrypoint,
    "Labels": {
        "prin.task.toRemove": "true"
    },
    "Env": [
        "TRINO_USER=$trinoUser",
        "TRINO_GROUP=$trinoGroup",
        "TRINO_ENDPOINT=trino:8080",
        "TRINO_CATALOG=hive",
        "TRINO_SCHEMA=default",
        "TASK_SCOPE=$scope",
        "TASK_APIS_BASE_URL=http://task-apis"
    ],
    "NetworkingConfig": {
        "EndpointsConfig": {
            "$THIS_CONTAINER_NETWORK": {}
        }
    }
}
JSON
)"
    log_with_date "Container config for task: $spawnedContainerConfig"

    # create new container
    local spawnedContainerId="$(
        echo "$spawnedContainerConfig" |
        curl -s --unix-socket /var/run/docker.sock \
            -H "Content-Type: application/json" \
            -d @- \
            -X POST http://localhost/containers/create | 
        jq -r '.Id'
    )"
    log_with_date "Task container created"

    # start container
    curl -s --unix-socket /var/run/docker.sock -X POST \
        "http://localhost/containers/$spawnedContainerId/start"
    log_with_date "Task container started, remove it with \`docker container rm $spawnedContainerId\`"
}

/opt/kafka/bin/kafka-console-consumer.sh \
    --bootstrap-server $KAFKA_BOOTSTRAP_SERVER \
    --topic "devprin.task.trigger" | \
while read -r msg
do
    log_with_date "Message received: $msg"
    start_container "$msg"
done