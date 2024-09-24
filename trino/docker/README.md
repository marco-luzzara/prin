In order to build Trino container, you need to locally build it from the `master` branch in this [PR](https://github.com/trinodb/trino/pull/22675#pullrequestreview-2322984895), as it contains the Plugin for Ranger.

- Build it locally with Maven and Java 22.0.0+. I have used Java 23 (build 23+37-2369)

    ```bash
    cd {trino-repo}
    ./mvnw clean install -DskipTests
    ```

- Run the Docker build

    ```bash
    cd ./core/docker
    ./build.sh
    ```

The resulting image will be: `trino:{TRINO_VERSION}-SNAPSHOT-{ARCH}`.
