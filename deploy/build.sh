#!/bin/bash

echo "Build UI..."
cd deploy
TAG_NAME=$(echo ${CI_COMMIT_REF_NAME} | sed -e "s|\/|\_|g")
docker build -t gcr.io/predictmachines/alexey_nginx:${TAG_NAME} .
