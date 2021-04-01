#!/bin/bash

TARGET_DIR='python/lib/python3.8/scito-dependencies'
mkdir -p "${TARGET_DIR}"
pip install git+https://github.com/yelabucsf/scito.git#egg=scito -t "${TARGET_DIR}"
zip -r scito_layer.zip python
rm -r python/
