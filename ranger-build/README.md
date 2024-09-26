# Build Ranger images with Trino Integration

Ranger does not support the Trino plugin for the stable release (2.4 at the time of writing). So you need to clone the `master` branch and build it with docker:

```bash
git clone git@github.com:apache/ranger.git -b ranger-2.6 --depth=1 ranger
git reset --hard 301c8ff4155bb06b16037a2eb2bed237be4701c4
cd ranger
./ranger_in_docker up
```
