# Create TagSync Docker image

Dockerfiles have been [copied from the repo](https://github.com/apache/ranger/blob/release-ranger-2.6.0/dev-support/ranger-docker/Dockerfile.ranger-tagsync). Before building the image, download the tagsync package (inside the destination folder the current version is already present):

```bash
wget -O ./docker/ranger-2.6.0-tagsync.tar.gz https://downloads.apache.org/ranger/2.6.0/services/tagsync/ranger-2.6.0-tagsync.tar.gz
```
