#!/bin/bash

# Make sure Docker is installed
CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
mkdir -p "${CURR_DIR}"/../layers



docker run \
  -v "${PWD}":/var/task "lambci/lambda:build-python3.8" \
  /bin/bash -c "bash scito_layer.sh; bash bustools_layer.sh exit"

mv *tar.gz "${CURR_DIR}"/../layers/


