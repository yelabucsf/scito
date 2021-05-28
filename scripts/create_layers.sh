#!/bin/bash

# Make sure Docker is installed
CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
mkdir -p "${CURR_DIR}"/../layers


# scito layer
docker run -v "${PWD}":/var/task "lambci/lambda:build-python3.8" /bin/bash -c "bash scito_layer.sh; exit"

# bustools layer
#docker run  -v "${PWD}":/var/task "lambci/lambda:build-python3.8" /bin/bash -c "bash bustools_layer.sh; exit"

mv *zip "${CURR_DIR}"/../layers/




