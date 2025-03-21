# Install Tagsync

Tagsync is not enabled by default in the official Ranger image. It must be installed directly from the Github repository.

```bash
# from the root directory of this repo
# import the RANGER_VERSION
source .env
# clone ranger
git clone https://github.com/apache/ranger.git --branch "release-ranger-${RANGER_VERSION}" --depth=1 ../ranger
cd ../ranger
```

Then follow the instructions [here](https://github.com/apache/ranger/blob/release-ranger-2.6.0/dev-support/ranger-docker/README.md) (Change the release accordingly).

**Note**: to build ranger, first `git apply ranger-build.patch`.

