SHELL = /bin/bash

CREATE_CRT_SCRIPT_PATH=./create-crt.sh

.PHONY: create-crt create-udf-package

create-crt:
	cd https && \
	chmod +x ${CREATE_CRT_SCRIPT_PATH} && \
	${CREATE_CRT_SCRIPT_PATH}
	cp https/rootCA.crt docker/server/rootCA.crt

create-udf-package:
	cd plugins/anonymization-udfs && ./mvnw clean install
	cp -r plugins/anonymization-udfs/target/trino-anonymization-udfs-1.0 docker/server/trino-anonymization-udfs-1.0