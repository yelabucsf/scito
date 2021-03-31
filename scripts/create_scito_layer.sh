#!/bin/bash

# Make sure Docker is installed
CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
mkdir -p ${CURR_DIR}/../layers/scito_layer
cd ${CURR_DIR}/../layers/scito_layer
TARGET_DIR='python/lib/python3.8/scito-dependencies'
mkdir -p ${TARGET_DIR}

DEPENDENCY="pip install git+https://github.com/yelabucsf/scito.git#egg=scito -t ${TARGET_DIR}"
TAR_CMD="tar -czf scito_layer.tar.gz python"

docker run -v "$PWD":/var/task "lambci/lambda:build-python3.8" /bin/bash -c "${DEPENDENCY}; ${TAR_CMD}; exit"
