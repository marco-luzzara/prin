# Build Ranger images with Trino Integration

Ranger does not support the Trino plugin for the stable release (2.4 at the time of writing). So you need to clone the `master` branch and build it with docker:

```bash
git clone git@github.com:apache/ranger.git ranger # --depth=1 if you want to use the latest master release
git reset --hard 301c8ff4155bb06b16037a2eb2bed237be4701c4 
git -C ranger apply ranger-build.patch
export ENABLED_RANGER_SERVICES="trino"
cd ranger
./ranger_in_docker up
```

---

## Additional Services

The only tested service is Trino, we had to exclude `ranger-usersync` too. It might be possible to include other services by changing the `ranger/distro/pom.xml`. In the `ranger-jdk11` maven profile, the only artifact produced are the one described by:

```
<descriptor>src/main/assembly/admin-web.xml</descriptor>
<descriptor>src/main/assembly/solr_audit_conf.xml</descriptor>
<descriptor>src/main/assembly/plugin-trino.xml</descriptor>
```

However, for the `all` maven profile (see above in the file), many other descriptors are present. The idea is to identify the ones you need and copy them to the `ranger-jdk11` profile. This is untested with JDK11. 

