#!/bin/bash

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
for layer in "${CURR_DIR}"/../layers/*
do
  BASE_NAME=$(basename -- ${layer})
  aws lambda publish-layer-version \
    --layer-name "${BASE_NAME%.zip}" \
    --description "Layers for scito-count architecture" \
    --content S3Bucket=ucsf-genomics-prod-project-data,S3Key=anton/scito/scito_count/layers/"${BASE_NAME}" \
    --compatible-runtimes "python3.8"
done