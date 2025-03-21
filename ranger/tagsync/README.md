# Create TagSync Docker image

Requirements: `ranger-base` docker image must be available locally and its version must be the same as the tagsync image version you want to create. See `../build-docker/README.md`.

Then modify the `Dockerfile.ranger-tagsync` in the ranger repo to allow configs customization through bind-mount volumes. See `ranger/tagsync/docker/Dockerfile`.