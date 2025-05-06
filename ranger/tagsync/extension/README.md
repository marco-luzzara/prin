# Tagsync Extension

This extension must be built starting from the Ranger repository. The current version is 2.6.0:

```bash
git clone git@github.com:apache/ranger.git --depth=1 --branch=release-ranger-2.6.0
cd ranger
```

Then apply the patch file you find in this repo:

```bash
git apply path/to/tagsync-ext-build.patch
```

Copy the `tagsync-extension` folder in the root path of the Ranger repository and run:

```bash
ranger_in_docker up
```

After the build, if successful, you can find a `JAR` file inside the `tagsync-extension/target` folder. Copy the Jar file in `../docker` folder, replacing the current one.