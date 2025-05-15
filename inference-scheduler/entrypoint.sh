#!/bin/bash

function start_container {
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
        "TRINO_USER=$1"
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
    echo "$(date -u +"%Y-%m-%dT%H:%M:%S") - Inference container created"

    # start container
    curl -s --unix-socket /var/run/docker.sock -X POST \
        "http://localhost/containers/$SPAWNED_CONTAINER_ID/start"
    echo "$(date -u +"%Y-%m-%dT%H:%M:%S") - Inference container started"
}

/opt/kafka/bin/kafka-console-consumer.sh \
    --bootstrap-server $KAFKA_BOOTSTRAP_SERVER \
    --topic $KAFKA_TOPIC_NAME | \
while read -r msg
do
    echo "Message received: $msg"
    trinoUser="$(echo "$msg" | jq -r '.username')"
    start_container "$trinoUser"
done