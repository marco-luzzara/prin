#!/bin/bash

function help {
cat <<EOF
Initialize Ranger with 4 roles and 2 users per role:

-----------------------------------------------------------------
| Role          | User                  | Password              |
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

These roles are configured with different policies:

-----------------------------------------------------------------
| Role          | Anonymized fields                             |
-----------------------------------------------------------------
| specialistdoc | telefono                                      |
|               |                                               |
-----------------------------------------------------------------
| researcher    | data_di_nascita, luogo_di_nascita, telefono,  |
|               | prima_visita, data_diagnosi                   |
-----------------------------------------------------------------
| careworker    | luogo_di_nascita, telefono, a, t, n           |
|               |                                               |
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

function _get_policy_resource {
    printf "{
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
            \"values\": [\"$1\"]
        }
    }"
}

function main {
    dpkg -s jq > /dev/null || { echo "Please first install jq"; exit 1; }

    for roleName in "specialistdoc" "researcher" "careworker" "nurse"
    do
        # create 2 users per role
        for i in 1 2
        do
            echo "Creating user ${roleName}_user${i}..."
            curl -X 'POST' "$ENDPOINT/service/xusers/secure/users" \
                -H 'accept: application/json' \
                -H 'Content-Type: application/json' \
                -u "$CREDENTIALS" \
                -d "{
                    \"name\": \"${roleName}_user${i}\",
                    \"password\": \"${roleName^}_user${i}\",
                    \"firstName\": \"user${i}\",
                    \"userRoleList\": [
                        \"ROLE_USER\"
                    ]
                }"
            echo -e "\nCreated user ${roleName}_user${i}"
        done

        # create role
        echo "Creating role ${roleName}..."
        curl -X 'POST' "$ENDPOINT/service/roles/roles" \
            -H 'Accept: application/json' \
            -H 'Content-Type: application/json' \
            -u "$CREDENTIALS" \
            -d "{
                \"name\": \"${roleName}\",
                \"users\": [
                    {
                        \"name\": \"${roleName}_user1\",
                        \"isAdmin\": false
                    },
                    {
                        \"name\": \"${roleName}_user2\",
                        \"isAdmin\": false
                    }
                ]
            }"
        echo -e "\nCreated role ${roleName}"
    done
    
    # create policies
    ## general access policies

    echo "Creating policy roles_policy..."
    curl -X 'POST' "$ENDPOINT/service/plugins/policies" \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -u "$CREDENTIALS" \
        -d "{
            \"allowExceptions\": [],
            \"policyItems\": [
                {
                    \"accesses\": [
                        {
                            \"type\": \"impersonate\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"execute\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"select\",
                            \"isAllowed\": true
                        }
                    ],
                    \"roles\": [\"specialistdoc\", \"researcher\", \"careworker\", \"nurse\"]
                }
            ],
            \"denyPolicyItems\": [],
            \"denyExceptions\": [],
            \"dataMaskPolicyItems\": [],
            \"rowFilterPolicyItems\": [],
            \"description\": \"\",
            \"isAuditEnabled\": true,
            \"isDenyAllElse\": false,
            \"isEnabled\": true,
            \"name\": \"roles_policy\",
            \"policyLabels\": [],
            \"policyPriority\": \"0\",
            \"policyType\": \"0\",
            \"service\": \"dev_trino\",
            \"resources\": {
                \"catalog\": {
                    \"values\": [\"*\"],
                    \"isExcludes\": false
                },
                \"schema\": {
                    \"values\": [\"*\"],
                    \"isExcludes\": false
                },
                \"table\": {
                    \"values\": [\"*\"],
                    \"isExcludes\": false
                },
                \"column\": {
                    \"values\": [\"*\"],
                    \"isExcludes\": false
                }
            },
            \"additionalResources\": [
                {
                    \"queryid\": {
                        \"values\": [\"*\"]
                    }
                },
                {
                    \"trinouser\": {
                        \"values\": [\"*\"]
                    }
                }
            ],
            \"conditions\": []
        }"
    echo -e "\nCreated policy roles_policy"

    ## specialistdoc policies
    echo "Creating policy mask_specialistdoc..."
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
                    \"roles\": [\"specialistdoc\"],
                    \"dataMaskInfo\": {
                        \"dataMaskType\": \"CUSTOM\",
                        \"valueExpr\": \"show_first_and_last({col})\"
                    }
                }
            ],
            \"rowFilterPolicyItems\": [],
            \"description\": \"\",
            \"isAuditEnabled\": true,
            \"isDenyAllElse\": false,
            \"isEnabled\": true,
            \"name\": \"mask_specialistdoc\",
            \"policyLabels\": [],
            \"policyPriority\": \"0\",
            \"policyType\": \"1\",
            \"service\": \"dev_trino\", 
            \"resources\": $(_get_policy_resource "telefono"),
            \"additionalResources\": [],
            \"conditions\":[]
        }"
    echo -e "\nCreated policy mask_specialistdoc"

    ## researcher policies
    echo "Creating policy mask_researcher..."
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
                    \"roles\": [\"researcher\"],
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
            \"name\": \"mask_researcher\",
            \"policyLabels\": [],
            \"policyPriority\": \"0\",
            \"policyType\": \"1\",
            \"service\": \"dev_trino\", 
            \"resources\": $(_get_policy_resource "data_di_nascita"),
            \"additionalResources\": [
                $(_get_policy_resource "luogo_di_nascita"),
                $(_get_policy_resource "telefono"),
                $(_get_policy_resource "prima_visita"),
                $(_get_policy_resource "data_diagnosi")
            ],
            \"conditions\":[]
        }"
    echo -e "\nCreated policy mask_researcher"

    ## careworker policies
    echo "Creating policy mask_careworker..."
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
                            \"isAllowed\": true
                        }
                    ],
                    \"roles\": [\"careworker\"],
                    \"dataMaskInfo\": {
                        \"dataMaskType\": \"MASK_HASH\"
                    }
                }
            ],
            \"rowFilterPolicyItems\": [],
            \"description\": \"\",
            \"isAuditEnabled\": true,
            \"isDenyAllElse\": false,
            \"isEnabled\": true,
            \"name\": \"mask_careworker\",
            \"policyLabels\": [],
            \"policyPriority\": \"0\",
            \"policyType\": \"1\",
            \"service\": \"dev_trino\", 
            \"resources\": $(_get_policy_resource "luogo_di_nascita"),
            \"additionalResources\": [
                $(_get_policy_resource "telefono"),
                $(_get_policy_resource "a"),
                $(_get_policy_resource "t"),
                $(_get_policy_resource "n")
            ],
            \"conditions\":[]
        }"
    echo -e "\nCreated policy mask_careworker"

    ## nurse policies
    echo "Creating policy mask_nurse..."
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
                    \"roles\": [\"nurse\"],
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
            \"resources\": $(_get_policy_resource "data_di_nascita"),
            \"additionalResources\": [
                $(_get_policy_resource "luogo_di_nascita"),
                $(_get_policy_resource "telefono"),
                $(_get_policy_resource "egfr"),
                $(_get_policy_resource "prima_visita"),
                $(_get_policy_resource "data_diagnosi"),
                $(_get_policy_resource "patologia"),
                $(_get_policy_resource "a"),
                $(_get_policy_resource "t"),
                $(_get_policy_resource "n")
            ],
            \"conditions\":[]
        }"
    echo -e "\nCreated policy mask_nurse"
}

OPTS=$(getopt -o e:c:h --longoptions "endpoint:,credentials:,help" -n 'initialize_ranger.sh' -- "$@")
eval set -- "$OPTS"

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
            echo "ERROR! No option is matching"
            exit 1
            ;;
    esac
done

main