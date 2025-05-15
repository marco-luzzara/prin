#!/bin/bash

function log_with_date {
    local msg="$1"
    echo "$(date -u +"%Y-%m-%dT%H:%M:%S") - $msg"
}

function start_container {
    local trinoUser="$1"
    log_with_date "Inference started by user $trinoUser"

    # https://stackoverflow.com/a/78009946/5587393
    THIS_CONTAINER_ID="$(cat /proc/self/mountinfo | grep -m1 -oE 'docker/containers/([a-f0-9]+)/' |\
        xargs basename)"

    # the spawned container must be attached to the same network as this container
    # because it needs to reach trino (or any other service in the same Docker compose)
    THIS_CONTAINER_NETWORK="$(curl -s --unix-socket /var/run/docker.sock -X GET \
        "http://localhost/containers/$THIS_CONTAINER_ID/json" | \
        jq -r '.NetworkSettings.Networks | keys | .[0]')"

    # create new container
    SPAWNED_CONTAINER_ID="$(
    {
        curl -s --unix-socket /var/run/docker.sock \
        -H "Content-Type: application/json" \
        -d @- \
        -X POST http://localhost/containers/create <<JSON
{
    "Image": "$INFERENCE_DOCKER_IMAGE",
    "Cmd": ["python", "main.py"],
    "Env": [
        "TRINO_USER=$trinoUser"
    ],
    "NetworkingConfig": {
        "EndpointsConfig": {
            "$THIS_CONTAINER_NETWORK": {}
        }
    }
}
JSON
    } | jq -r '.Id'
    )"
    log_with_date "Inference container created"

    # start container
    curl -s --unix-socket /var/run/docker.sock -X POST \
        "http://localhost/containers/$SPAWNED_CONTAINER_ID/start"
    log_with_date "Inference container started, remove it with \`docker container rm $SPAWNED_CONTAINER_ID\`"
}

/opt/kafka/bin/kafka-console-consumer.sh \
    --bootstrap-server $KAFKA_BOOTSTRAP_SERVER \
    --topic $KAFKA_TOPIC_NAME | \
while read -r msg
do
    log_with_date "Message received: $msg"
    trinoUser="$(echo "$msg" | jq -r '.username')"
    start_container "$trinoUser"
done