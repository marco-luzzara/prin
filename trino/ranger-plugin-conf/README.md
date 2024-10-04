# Configure Trino with Ranger Plugin 

- Clone the Trino repo (not in this folder) and compile it with:

```bash
git clone git@github.com:mneethiraj/trino.git .

./mvnw clean install -DskipTests -pl plugin/trino-ranger -am
```

This will only compile the ranger-plugin (and the required dependency projects) and produces `plugin/trino-ranger/target/trino-ranger-${TRINO_VERSION}-SNAPSHOT.zip`.

```bash
cd plugin/trino-ranger/target

# there should already be the unzipped dir, else run
# $ unzip trino-ranger-${TRINO_VERSION}-SNAPSHOT.zip

cp -r trino-ranger-${TRINO_VERSION}-SNAPSHOT trino-ranger-plugin
```

Copy the `trino-ranger-plugin` in the `trino/docker` folder:

```bash
cp -r trino-ranger-plugin /home/.../trino/docker
```
