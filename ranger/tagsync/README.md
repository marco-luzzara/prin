# Create TagSync Docker image

Dockerfiles have been [copied from the repo](https://github.com/apache/ranger/blob/release-ranger-2.6.0/dev-support/ranger-docker/Dockerfile.ranger-tagsync). Before building the image, download the tagsync package (inside the destination folder the current version is already present):

```bash
wget -O ./docker/ranger-2.6.0-tagsync.tar.gz https://downloads.apache.org/ranger/2.6.0/services/tagsync/ranger-2.6.0-tagsync.tar.gz
```

The Jar does not contain all the necessary resources, despite being a uber jar. The additional jars that must be installed are:

```
com.google.guava:guava:25.1-jre
```

The `docker/ranger-tagsync.sh` script must be updated to include this dependency. After the `.setupDone` file is created (line 32), add the following commands:

```bash
wget -O "${RANGER_HOME}/ranger-2.6.0-tagsync/lib/guava-25.1-jre.jar" https://repo1.maven.org/maven2/com/google/guava/guava/25.1-jre/guava-25.1-jre.jar
chmod 755 "${RANGER_HOME}/ranger-2.6.0-tagsync/lib/guava-25.1-jre.jar"
```