FROM trino:459-SNAPSHOT-amd64

COPY rootCA.crt /etc/pki/ca-trust/source/anchors/

USER root

RUN <<EOF
    cd /usr/lib/trino/plugin/ranger
    ln -s /etc/trino conf

    # add CA certificate to your system store
    update-ca-trust extract

    # add CA certificate to Java keystore
    KEYSTORE_PASSWORD=changeit
    keytool -import -trustcacerts -alias root-ca -file /etc/pki/ca-trust/source/anchors/rootCA.crt -keystore "$JAVA_HOME/lib/security/cacerts" -storepass "$KEYSTORE_PASSWORD" -noprompt
    keytool -import -trustcacerts -alias root-ca -file /etc/pki/ca-trust/source/anchors/rootCA.crt -keystore /etc/pki/java/cacerts -storepass "$KEYSTORE_PASSWORD" -noprompt
EOF

USER trino:trino