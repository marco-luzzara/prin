#!/bin/bash

function create_rootCA_crt {
    # create root CA cert
    openssl req -x509 \
                -sha256 -days 35600 \
                -noenc \
                -newkey rsa:2048 \
                -subj "/CN=localhost/C=IT/L=Milan/O=Prin" \
                -keyout rootCA.key -out rootCA.crt 
}

function create_server_pem {
    # Create the server private key
    openssl genrsa -out server.key 2048

    # Create the CSR
    openssl req -new -key server.key -out server.csr -config csr.conf

    # Create the Certificate
    openssl x509 -req \
        -in server.csr \
        -CA rootCA.crt -CAkey rootCA.key \
        -CAcreateserial -out server.crt \
        -days 36500 \
        -sha256 -extfile cert.conf

    # Create server.pem, as required by Trino (https://trino.io/docs/current/security/inspect-pem.html)
    cat server.key server.crt > server.pem
}

test -e rootCA.crt && echo "the rootCA.crt already exists." || create_rootCA
test -e server.pem && echo "the server.pem already exists." || create_server_pem

# Validate server.pem
openssl rsa -in server.pem -check -noout || { echo "the .pem file is not valid, delete it and re-run the script." ; exit 1; }

echo "Certificates created successfully. Use the server.pem and the CA certificate (rootCA.crt)"