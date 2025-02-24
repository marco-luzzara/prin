ARG TRINO_VERSION

FROM trinodb/trino:${TRINO_VERSION}

COPY rootCA.crt /etc/pki/ca-trust/source/anchors/

# install plugins
COPY trino-anonymization-udfs-1.0/ /usr/lib/trino/plugin/anonymization-udfs/

# install root CA certificates 
USER root

RUN <<EOF
    # add CA certificate to your system store
    update-ca-trust extract

    # add CA certificate to Java keystore
    KEYSTORE_PASSWORD=changeit
    keytool -import -trustcacerts -alias root-ca -file /etc/pki/ca-trust/source/anchors/rootCA.crt -keystore "$JAVA_HOME/lib/security/cacerts" -storepass "$KEYSTORE_PASSWORD" -noprompt
    keytool -import -trustcacerts -alias root-ca -file /etc/pki/ca-trust/source/anchors/rootCA.crt -keystore /etc/pki/java/cacerts -storepass "$KEYSTORE_PASSWORD" -noprompt
EOF

USER trino:trino