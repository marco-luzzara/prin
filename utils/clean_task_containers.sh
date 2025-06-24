#!/bin/bash -e

terminatedTaskIds="$(docker container ls -a \
    --filter "label=prin.task.toRemove=true" \
    --filter "status=exited" \
    --format "{{.ID}}" | \
    sed -z 's/\n/ /g')"

echo "Removing containers $terminatedTaskIds"
docker container rm $terminatedTaskIds
echo "Containers $terminatedTaskIds terminated successfully"
