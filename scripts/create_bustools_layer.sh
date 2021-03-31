#!/bin/bash

# Make sure Docker is installed
BUSTOOLS_GIT="https://github.com/BUStools/bustools.git"

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
mkdir -p ${CURR_DIR}/../layers/bustools_layer
cd ${CURR_DIR}/../layers/bustools_layer

GIT_CLONE="git clone ${BUSTOOLS_GIT}"
COMPILE_BUSTOOLS="cd bustools && mkdir build && cd build && cmake .. && make"
SHARED_LIBS="ldd"

TAR_CMD="tar -czvfp bustools_layer.tar.gz python/"

docker run -v "$PWD":/var/task "lambci/lambda:build-python3.8" /bin/bash -c "${GIT_CLONE}; ${COMPILE_BUSTOOLS}; exit"
