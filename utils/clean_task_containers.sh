#!/bin/bash -e

terminatedTaskIds="$(docker container ls -a \
    --filter "label=prin.task.toRemove=true" \
    --filter "status=exited" \
    --format "{{.ID}}" | \
    sed -z 's/\n/ /g')"

if [[ -z $terminatedTaskIds ]]
then
    echo "There is no task container to remove."
    exit 0
fi

echo "Removing containers $terminatedTaskIds"
docker container rm $terminatedTaskIds
echo "Containers $terminatedTaskIds terminated successfully"
