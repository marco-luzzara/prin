# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Copied from https://github.com/apache/ranger/blob/release-ranger-2.6.0/dev-support/ranger-docker/Dockerfile.ranger-base

ARG UBUNTU_VERSION=20.04
FROM ubuntu:${UBUNTU_VERSION} AS ranger-base

ARG TARGETARCH
ARG RANGER_BASE_JAVA_VERSION=8
ENV OS_NAME=UBUNTU

# Install tzdata, Python, Java, python-requests
RUN apt-get update && \
    DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata vim\
    python3 python3-pip openjdk-8-jdk openjdk-11-jdk openjdk-17-jdk bc iputils-ping ssh pdsh xmlstarlet && \
    pip3 install apache-ranger && \
    pip3 install requests

# Set environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-${RANGER_BASE_JAVA_VERSION}-openjdk-${TARGETARCH}
ENV RANGER_DIST=/home/ranger/dist
ENV RANGER_SCRIPTS=/home/ranger/scripts
ENV RANGER_HOME=/opt/ranger
ENV PATH=/usr/java/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

RUN update-java-alternatives --set /usr/lib/jvm/java-1.${RANGER_BASE_JAVA_VERSION}.0-openjdk-${TARGETARCH}

# setup groups, users, directories
RUN groupadd ranger && \
    useradd -g ranger -ms /bin/bash ranger && \
    useradd -g ranger -ms /bin/bash rangeradmin && \
    useradd -g ranger -ms /bin/bash rangerusersync && \
    useradd -g ranger -ms /bin/bash rangertagsync && \
    useradd -g ranger -ms /bin/bash rangerkms && \
    groupadd hadoop && \
    useradd -g hadoop -ms /bin/bash hdfs && \
    useradd -g hadoop -ms /bin/bash yarn && \
    useradd -g hadoop -ms /bin/bash hive && \
    useradd -g hadoop -ms /bin/bash hbase && \
    useradd -g hadoop -ms /bin/bash kafka && \
    useradd -g hadoop -ms /bin/bash ozone && \
    groupadd knox && \
    useradd -g knox -ms /bin/bash knox && \
    mkdir -p /home/ranger/dist && \
    mkdir -p /home/ranger/scripts && \
    chown -R ranger:ranger /home/ranger && \
    mkdir -p /opt/ranger && \
    chown -R ranger:ranger /opt/ranger

ENTRYPOINT [ "/bin/bash" ]

FROM ranger-base AS ranger-tagsync

ARG TAGSYNC_VERSION=2.6.0

# COPY ./dist/version                                  /home/ranger/dist/
COPY ./ranger-${TAGSYNC_VERSION}-tagsync.tar.gz /home/ranger/dist/

COPY ./ranger-tagsync.sh                     ${RANGER_SCRIPTS}/
# COPY ./scripts/ranger-tagsync-install.properties     ${RANGER_SCRIPTS}/
# COPY ./scripts/ranger-tagsync-tags.json              ${RANGER_SCRIPTS}/

RUN <<EOF
    tar xvfz /home/ranger/dist/ranger-${TAGSYNC_VERSION}-tagsync.tar.gz --directory=${RANGER_HOME}
    ln -s ${RANGER_HOME}/ranger-${TAGSYNC_VERSION}-tagsync ${RANGER_HOME}/tagsync
    rm -f /home/ranger/dist/ranger-${TAGSYNC_VERSION}-tagsync.tar.gz
    mkdir -p /opt/ranger/tagsync/data
    # cp -f ${RANGER_SCRIPTS}/ranger-tagsync-install.properties ${RANGER_HOME}/tagsync/install.properties
    # cp -f ${RANGER_SCRIPTS}/ranger-tagsync-tags.json ${RANGER_HOME}/tagsync/data/tags.json
    mkdir -p /var/run/ranger
    mkdir -p /var/log/ranger/tagsync
    ln -s /usr/bin/python3 /usr/bin/python
    mkdir -p /etc/ranger
    mkdir /etc/init.d || true
    mkdir /etc/rc2.d  || true
    mkdir /etc/rc3.d  || true
    touch /etc/init.d/ranger-tagsync
    ln -s /etc/init.d/ranger-tagsync /etc/rc2.d/S99ranger-tagsync
    ln -s /etc/init.d/ranger-tagsync /etc/rc2.d/K00ranger-tagsync
    ln -s /etc/init.d/ranger-tagsync /etc/rc3.d/S99ranger-tagsync
    ln -s /etc/init.d/ranger-tagsync /etc/rc3.d/K00ranger-tagsync
    ln -s ${RANGER_HOME}/tagsync/ranger-tagsync-services.sh /usr/bin/ranger-tagsync-services.sh
    chown -R ranger:ranger ${RANGER_HOME}/tagsync/ ${RANGER_SCRIPTS}/ /var/run/ranger/ /var/log/ranger/ /etc/ranger /etc/init.d/ranger-tagsync
    chmod 744 ${RANGER_SCRIPTS}/ranger-tagsync.sh
EOF

COPY ./ranger-tagsync-extension-${TAGSYNC_VERSION}.jar /opt/ranger/ranger-${TAGSYNC_VERSION}-tagsync/dist/

USER ranger

ENTRYPOINT [ "/home/ranger/scripts/ranger-tagsync.sh" ]
