#!/bin/bash

# Make sure Docker is installed
ROOT_DIR=${PWD}
BUSTOOLS_GIT="https://github.com/BUStools/bustools.git"
mkdir -p "${ROOT_DIR}"/bustools/{bin,lib}

git clone "${BUSTOOLS_GIT}" "${ROOT_DIR}"/bustools_git/
cd bustools_git && mkdir build && cd build && cmake .. && make
ldd "${ROOT_DIR}"/bustools_git/build/src/bustools | grep "=> /" | awk '{print $3}' | xargs -I '{}' cp -v '{}' "${ROOT_DIR}"/bustools/lib
cp "${ROOT_DIR}"/bustools_git/build/src/bustools "${ROOT_DIR}"/bustools/bin
cd "${ROOT_DIR}"
tar -czf bustools_layer.tar.gz bustools/

rm -r {bustools_git,bustools}



