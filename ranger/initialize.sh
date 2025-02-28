#!/bin/bash

function help {
    cat <<EOF
        Initialize Ranger with 3 groups and 2 users per group:

        -----------------------------------------------------------------
        | Group         | User                  | Password              |
        -----------------------------------------------------------------
        | specialistdoc | specialistdoc_user1   | Specialistdoc_user1   |
        |               | specialistdoc_user2   | Specialistdoc_user2   |
        -----------------------------------------------------------------
        | researcher    | researcher_user1      | Researcher_user1      |
        |               | researcher_user2      | Researcher_user2      |
        -----------------------------------------------------------------
        | careworker    | careworker_user1      | Careworker_user1      |
        |               | careworker_user2      | Careworker_user2      |
        -----------------------------------------------------------------
        | nurse         | nurse_user1           | Nurse_user1           |
        |               | nurse_user2           | Nurse_user2           |
        -----------------------------------------------------------------

        These groups are configured with different policies:

        -----------------------------------------------------------------
        | Group         | Anonymized fields                             |
        -----------------------------------------------------------------
        | specialistdoc | -                                             |
        |               |                                               |
        -----------------------------------------------------------------
        | researcher    | data_di_nascita, luogo_di_nascita, telefono,  |
        |               | prima_visita, data_diagnosi                   |
        -----------------------------------------------------------------
        | careworker    | data_di_nascita, luogo_di_nascita, telefono,  |
        |               | prima_visita, a, t, n                         |
        -----------------------------------------------------------------
        | nurse         | data_di_nascita, luogo_di_nascita, telefono,  |
        |               | egfr, prima_visita, data_diagnosi, patologia, |
        |               | a, t, n                                       |
        -----------------------------------------------------------------

        Options:
            - --endpoint <url>                  ranger endpoint (e.g. http://localhost:6080)
            - --credentials <user:password>     User credentials in the form "username:password"
            - --help                            shows this help message

        Example:

            ./initialize.sh --endpoint http://localhost:6080 --credentials "admin:rangerR0cks!"
    EOF
}

function main {
    dpkg -s jq || { echo "Please first install jq"; exit 1; }

    for groupName in "specialistdoc" "researcher" "careworker" "nurse"
    do
        # create group if not exists
        GROUP_ID=$(curl -s -X 'GET' "$ENDPOINT/service/xusers/groups/groupName/$groupName" \
            -H 'accept: application/json' \
            -u "$CREDENTIALS" | jq -r ".id")
        if [[ $GROUP_ID == null ]]
        then
            curl -X 'POST' "$ENDPOINT/service/xusers/groups" \
                -H 'accept: application/json' \
                -H 'Content-Type: application/json' \
                -u "$CREDENTIALS" \
                -d "{
                    \"name\": \"$groupName\"
                }"
            
            # create two users per group
            for i in 1 2
            do
                curl -X 'POST' "$ENDPOINT/service/xusers/secure/users" \
                    -H 'accept: application/json' \
                    -H 'Content-Type: application/json' \
                    -u "$CREDENTIALS" \
                    -d "{
                        \"name\": \"${groupName}_user${i}\",
                        \"password\": \"${groupName^}_user${i}\",
                        \"firstName\": \"user${i}\",
                        \"userRoleList\": [
                            \"ROLE_USER\"
                        ],
                        \"groupIdList\": [
                            $GROUP_ID
                        ]
                    }"
            done
        fi
    done
    
    # create policies
    curl -X 'POST' "$ENDPOINT/service/plugins/policies" \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -u "$CREDENTIALS" \
        -d "{
            \"allowExceptions\": [],
            \"policyItems\": [],
            \"denyPolicyItems\": [],
            \"denyExceptions\": [],
            \"dataMaskPolicyItems\": [
                {
                    \"accesses\": [
                        {
                            \"type\":\"select\",
                            \"isAllowed\":true
                        }
                    ],
                    \"groups\": [\"researcher\",\"nurse\"],
                    \"dataMaskInfo\": {
                        \"dataMaskType\":\"MASK_NULL\"
                    }
                }
            ],
            \"rowFilterPolicyItems\": [],
            \"description\": \"\",
            \"isAuditEnabled\": true,
            \"isDenyAllElse\": false,
            \"isEnabled\": true,
            \"name\": \"mask_nurse\",
            \"policyLabels\": [],
            \"policyPriority\": \"0\",
            \"policyType\": \"1\",
            \"service\": \"dev_trino\", 
            \"resources\": {
                \"catalog\": {
                    \"values\": [\"hive\"]
                },
                \"schema\": {
                    \"values\": [\"default\"]
                },
                \"table\": {
                    \"values\": [\"patient_records\"]
                },
                \"column\": {
                    \"values\": [\"data_di_nascita\"]
                }
            },
            \"additionalResources\": [],
            \"conditions\":[]
        }'
}

TEMP=$(getopt --long "endpoint:,credentials:,help:" -n 'initialize_ranger.sh' -- "$@")
eval set -- "$TEMP"

while true; do
    case "$1" in
        --help)
            file="$2"
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
            echo "No option is matching"
            exit 1
            ;;
    esac
done

main