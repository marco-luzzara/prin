To enable password authentication in Trino, we need to enable HTTPS first. To configure Trino with TLS support, consider two alternative paths:

- Use the load balancer or proxy at your site or cloud environment to terminate TLS/HTTPS. This approach is the simplest and strongly preferred solution.
- Secure the Trino server directly. This requires you to obtain a valid certificate, and add it to the Trino coordinator’s configuration.

Find more info [here](https://trino.io/docs/current/security/tls.html). For development, we can use our own self-signed certificated [(guide)](https://devopscube.com/create-self-signed-certificates-openssl/):

- Create the root CA certificate:

```bash
openssl req -x509 \
            -sha256 -days 35600 \
            -noenc \
            -newkey rsa:2048 \
            -subj "/CN=localhost/C=IT/L=Milan/O=Prin" \
            -keyout rootCA.key -out rootCA.crt 
```

- Create the server private key:

```bash
openssl genrsa -out server.key 2048
```

- Create the CSR:

```bash
openssl req -new -key server.key -out server.csr -config csr.conf
```

- Create the Certificate

```bash
openssl x509 -req \
    -in server.csr \
    -CA rootCA.crt -CAkey rootCA.key \
    -CAcreateserial -out server.crt \
    -days 36500 \
    -sha256 -extfile cert.conf
```

Trino needs a PEM file, as described [here](https://trino.io/docs/current/security/inspect-pem.html):

```bash
cat server.key server.crt > server.pem
```

Validate it with:

```bash
openssl rsa -in server.pem -check -noout
```

---

Now you can access trino with cli using https endpoint:

```bash
trino --server https://localhost:8443 --user test_user1 --password
```

And test it with:

```
SELECT 'rocks' AS trino;
```