#!/bin/bash

function help {
cat <<EOF
**Created Resources**
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

These roles are configured with different policies:

-----------------------------------------------------------------
| Role          | Anonymized fields                             |
-----------------------------------------------------------------
| specialistdoc |                                               |
|               |                                               |
-----------------------------------------------------------------
| researcher    | first_visit, diagnose_date                    |
|               |                                               |
-----------------------------------------------------------------
| careworker    | iadl, egfr                                    |
|               |                                               |
-----------------------------------------------------------------

It also creates the Atlas service.

**Options**
    - --endpoint <url>                  ranger endpoint (e.g. http://localhost:6080)
    - --credentials <user:password>     User credentials in the form "username:password"
    - --help                            shows this help message

**Example**

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
            \"values\": [\"patients\"]
        },
        \"column\": {
            \"values\": [\"$1\"]
        }
    }"
}

function create_users_and_roles {
    for roleName in "specialistdoc" "researcher" "careworker"
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
}

function create_policies {
    # Policy examples:
    # - custom policy using a trino UDF
        # \"dataMaskInfo\": {
        #     \"dataMaskType\": \"CUSTOM\",
        #     \"valueExpr\": \"show_first_and_last({col})\"
        # }
    # - fields are nullified
        # \"dataMaskInfo\": {
        #     \"dataMaskType\":\"MASK_NULL\"
        # }
    # - fields are hashed
        # \"dataMaskInfo\": {
        #     \"dataMaskType\": \"MASK_HASH\"
        # }
    # - only year is shown in date fields
        # \"dataMaskInfo\": {
        #     \"dataMaskType\": \"MASK_DATE_SHOW_YEAR\"
        # }

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

    # atlas tag-based policy
    echo "Creating tag_based_policy..."
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
                            \"type\": \"type-create\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"type-delete\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"type-read\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"type-update\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"entity-read\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"entity-create\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"entity-update\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"entity-delete\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"admin-purge\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"admin-import\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"admin-export\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"admin-audits\",
                            \"isAllowed\": true
                        }
                    ],
                    \"roles\": [
                        \"specialistdoc\",
                        \"researcher\",
                        \"careworker\"
                    ]
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
            \"name\": \"tag_based_policy\",
            \"policyLabels\": [],
            \"policyPriority\": \"0\",
            \"policyType\": \"0\",
            \"service\": \"dev_atlas\",
            \"resources\": {
                \"type-category\": {
                    \"values\": [\"*\"],
                    \"isExcludes\": false
                },
                \"type\": {
                    \"values\": [\"*\"],
                    \"isExcludes\": false
                }
            },
            \"additionalResources\": [
                {
                    \"entity-type\": {
                        \"values\": [\"*\"],
                        \"isExcludes\": false
                    },
                    \"entity-classification\": {
                        \"values\": [\"*\"],
                        \"isExcludes\": false
                    },
                    \"entity\": {
                        \"values\": [\"*\"],
                        \"isExcludes\": false
                    }
                },
                {
                    \"atlas-service\": {
                        \"values\": [\"atlas-service\"],
                        \"isExcludes\": false
                    }
                }
            ],
            \"conditions\": []
        }"
    echo -e "\nCreated tag_based_policy"

    echo "Creating policy allow_access_TEST_CLASS..."
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
                            \"type\": \"trino:select\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"trino:insert\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"trino:create\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"trino:drop\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"trino:delete\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"trino:use\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"trino:alter\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"trino:grant\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"trino:revoke\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"trino:show\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"trino:impersonate\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"trino:all\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"trino:execute\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"trino:read_sysinfo\",
                            \"isAllowed\": true
                        },
                        {
                            \"type\": \"trino:write_sysinfo\",
                            \"isAllowed\": true
                        }
                    ],
                    \"roles\": [
                        \"specialistdoc\",
                        \"researcher\",
                        \"careworker\"
                    ],
                    \"conditions\": []
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
            \"name\": \"allow_access_TEST_CLASS\",
            \"policyLabels\": [],
            \"policyPriority\": \"0\",
            \"policyType\": \"0\",
            \"service\": \"dev_tag\",
            \"resources\": {
                \"tag\": {
                    \"values\": [
                        \"TEST_CLASS\"
                    ]
                }
            },
            \"additionalResources\": [],
            \"conditions\": []
        }"
    echo -e "\nCreated policy allow_access_TEST_CLASS"

    echo "Creating policy mask_TEST_CLASS ..."
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
                            \"type\": \"trino:select\",
                            \"isAllowed\": true
                        }
                    ],
                    \"roles\": [
                        \"specialistdoc\",
                        \"researcher\",
                        \"careworker\"
                    ],
                    \"dataMaskInfo\": {
                        \"dataMaskType\": \"trino:MASK_NULL\"
                    }
                }
            ],
            \"rowFilterPolicyItems\": [],
            \"description\": \"\",
            \"isAuditEnabled\": true,
            \"isDenyAllElse\": false,
            \"isEnabled\": true,
            \"name\": \"mask_TEST_CLASS\",
            \"policyLabels\": [],
            \"policyPriority\": \"0\",
            \"policyType\": \"1\",
            \"service\": \"dev_tag\",
            \"resources\": {
                \"tag\": {
                    \"values\": [
                        \"TEST_CLASS\"
                    ]
                }
            },
            \"additionalResources\": [],
            \"conditions\": []
        }"
    echo -e "\nCreated policy mask_TEST_CLASS"

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
                        \"dataMaskType\":\"MASK_DATE_SHOW_YEAR\"
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
                $(_get_policy_resource "first_visit"),
                $(_get_policy_resource "diagnose_date")
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
                $(_get_policy_resource "iadl"),
                $(_get_policy_resource "egfr")
            ],
            \"conditions\":[]
        }"
    echo -e "\nCreated policy mask_careworker"
}

function create_additional_services {
    # update trino service
    TRINO_SERVICE_ID=$(curl -s -X 'GET' "$ENDPOINT/service/plugins/services/name/dev_trino" \
        -H 'accept: application/json' \
        -u "$CREDENTIALS" | jq -r '.id')
    
    curl -X 'PUT' "$ENDPOINT/service/plugins/services/$TRINO_SERVICE_ID" \
        -H 'Accept: application/json' \
        -H 'Content-Type: application/json' \
        -u "$CREDENTIALS" \
        -d "{
            \"id\": \"$TRINO_SERVICE_ID\",
            \"isEnabled\": true,
            \"type\": \"trino\",
            \"name\": \"dev_trino\",
            \"tagService\": \"dev_tag\",
            \"configs\": {
                \"username\":\"trino\",
                \"jdbc.driverClassName\": \"io.trino.jdbc.TrinoDriver\",
                \"jdbc.url\": \"jdbc:trino://trino:8080\",
                \"ranger.plugin.audit.filters\": \"[{'accessResult':'DENIED','isAudited':true},{'isAudited':false,'resources':{'queryid':{'values':['*']}},'accessTypes':['execute']},{'isAudited':false,'resources':{'trinouser':{'values':['{USER}']}},'accessTypes':['impersonate']}]\"
            }
        }"
    
    # create atlas service
    curl -X 'POST' "$ENDPOINT/service/plugins/services" \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -u "$CREDENTIALS" \
        -d "{
            \"name\": \"dev_atlas\",
            \"type\": \"atlas\",
            \"tagService\": \"\",
            \"isEnabled\": true,
            \"configs\": {
                \"username\": \"admin\",
                \"atlas.rest.address\": \"http://atlas:21000\",
                \"password\": \"admin\",
                \"ranger.plugin.audit.filters\": \"[{'accessResult':'DENIED','isAudited':true},{'users':['atlas'],'isAudited':false},{'accessResult':'ALLOWED','isAudited':false,'actions':['entity-read'],'accessTypes':['entity-read'],'users':['nifi']}]\"
            }
        }"
}

function main {
    dpkg -s jq > /dev/null || { echo "Please first install jq"; exit 1; }
    
    create_users_and_roles
    create_policies

    create_additional_services
}

OPTS=$(getopt -o e:c:h --longoptions "endpoint:,credentials:,help" -n 'initialize_ranger.sh' -- "$@")
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