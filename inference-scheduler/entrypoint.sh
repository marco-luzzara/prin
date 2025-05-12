#!/bin/bash

function start_container {
    CONTAINER_ID="$(curl -s --unix-socket /var/run/docker.sock -H "Content-Type: application/json" \
        -d "{\"Image\": \"$INFERENCE_DOCKER_IMAGE\", \"Cmd\": [\"python\", \"main.py\"]}" \
        -X POST http://localhost/containers/create | jq -r '.Id')"

    curl --unix-socket /var/run/docker.sock -X POST "http://localhost/containers/$CONTAINER_ID/start"
}

/opt/kafka/bin/kafka-console-consumer.sh \
    --bootstrap-server $KAFKA_BOOTSTRAP_SERVER \
    --topic $KAFKA_TOPIC_NAME | \
while read -r msg
do
    echo "Message received: $msg"
    start_container
done