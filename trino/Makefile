SHELL = /bin/bash

CREATE_CRT_SCRIPT_PATH=./https/create-crt.sh

.PHONY: create-crt create-udf-package

create-crt:
	chmod +x ${CREATE_CRT_SCRIPT_PATH}
	${CREATE_CRT_SCRIPT_PATH}

create-udf-package:
	cd plugins/anonymization-udfs && ./mvnw clean install
	cp -r plugins/anonymization-udfs/target/trino-anonymization-udfs-1.0 docker/server/trino-anonymization-udfs-1.0