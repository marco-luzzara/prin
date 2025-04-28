#!/bin/bash

function help {
cat <<EOF
**Created Resources**
Initialize Atlas with a single classification (and related attribute):

**Options**
    - --endpoint <url>                  atlas endpoint (e.g. http://localhost:21000)
    - --credentials <user:password>     User credentials in the form "username:password"
    - --help                            shows this help message

**Example**

    ./initialize.sh --endpoint http://localhost:21000 --credentials "admin:admin"
EOF
}

function main {
    dpkg -s jq > /dev/null || { echo "Please first install jq"; exit 1; }

    curl -X 'POST' "$ENDPOINT/api/atlas/v2/types/typedefs?type=classification" \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -u "$CREDENTIALS" \
        -d "{
                \"classificationDefs\": [
                    {
                        \"name\": \"TEST_CLASS\",
                        \"description\": \"<p>Classification for testing Atlas</p>\",
                        \"superTypes\": [],
                        \"attributeDefs\": [
                            {
                                \"name\": \"val\",
                                \"typeName\": \"int\",
                                \"isOptional\": true,
                                \"cardinality\": \"SINGLE\",
                                \"valuesMinCount\": 0,
                                \"valuesMaxCount\": 1,
                                \"isUnique\": false,
                                \"isIndexable\": true
                            }
                        ]
                    }
                ],
                \"entityDefs\": [],
                \"enumDefs\": [],
                \"structDefs\":[]
            }"

    AGE_ENTITY_GUID="$(curl -s "$ENDPOINT/api/atlas/v2/search/quick?query=age" \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -u "$CREDENTIALS" | jq -r '.searchResults.entities[0].guid' \
    )"
    
    curl -X 'POST' "$ENDPOINT/api/atlas/v2/entity/bulk/classification" \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -u "$CREDENTIALS" \
        -d "{
                \"classification\": {
                    \"typeName\": \"TEST_CLASS\",
                    \"attributes\": {
                        \"val\": \"100\"
                    },
                    \"propagate\":true,
                    \"removePropagationsOnEntityDelete\": false,
                    \"validityPeriods\": []
                },
                \"entityGuids\": [\"$AGE_ENTITY_GUID\"]
            }"
}

OPTS=$(getopt -o e:c:h --longoptions "endpoint:,credentials:,help" -n 'initialize_atlas.sh' -- "$@")
eval set -- "$OPTS"

while true; do
    case "$1" in
        --help)
            help
            exit 0
            ;;
        --endpoint)
            ENDPOINT="$2"
            shift 2
            ;;
        --credentials)
            CREDENTIALS="$2"
            shift 2
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "ERROR! No option is matching"
            exit 1
            ;;
    esac
done

main