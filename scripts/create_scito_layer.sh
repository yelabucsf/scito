#!/bin/bash

# Make sure Docker is installed
CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
TOKEN=cat ${CURR_DIR}/TOKEN.txt
mkdir -p ${CURR_DIR}/../layers/scito_layer
cd ${CURR_DIR}/../layers/scito_layer
mkdir -p python/lib/python3.8/scito-dependencies

DEPENDENCY="pip install git+https://github.com/yelabucsf/scito.git#egg=scito -t python/lib/python3.8/scito-dependencies/"

docker run -v "$PWD":/var/task "lambci/lambda:build-python3.8" /bin/bash -c "${DEPENDENCY}; exit"
