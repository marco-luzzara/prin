#!/bin/bash

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


if [ ! -e ${RANGER_HOME}/.setupDone ]
then
  SETUP_RANGER=true
else
  SETUP_RANGER=false
fi

if [ "${SETUP_RANGER}" == "true" ]
then
  cd "${RANGER_HOME}"/tagsync || exit
  if ./setup.sh;
  then
    touch "${RANGER_HOME}"/.setupDone
    # Missing dependency in the Uber jar of ranger-tagsync
    wget -O "${RANGER_HOME}/ranger-2.6.0-tagsync/lib/guava-25.1-jre.jar" https://repo1.maven.org/maven2/com/google/guava/guava/25.1-jre/guava-25.1-jre.jar
    chmod 755 "${RANGER_HOME}/ranger-2.6.0-tagsync/lib/guava-25.1-jre.jar"
  else
    echo "Ranger TagSync Setup Script didn't complete proper execution."
  fi
fi

cd ${RANGER_HOME}/tagsync && ./ranger-tagsync-services.sh start

RANGER_TAGSYNC_PID=`ps -ef  | grep -v grep | grep -i "org.apache.ranger.tagsync.process.TagSynchronizer" | awk '{print $2}'`

# prevent the container from exiting
if [ -z "$RANGER_TAGSYNC_PID" ]
then
  echo "The TagSync process probably exited, no process id found!"
else
  tail --pid=$RANGER_TAGSYNC_PID -f /dev/null
fi
