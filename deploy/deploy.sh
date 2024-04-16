#!/bin/bash

echo "Deploy..."
cd deploy
docker login -u oauth2accesstoken -p "$(gcloud auth application-default print-access-token)" https://gcr.io
TAG_NAME=$(echo ${CI_COMMIT_REF_NAME} | sed -e "s|\/|\_|g")
docker push gcr.io/predictmachines/alexey_nginx:${TAG_NAME}

export KUBECONFIG=/home/gitlab-runner/kube.yaml
# /snap/bin/kubectl apply -f nginx-deployment.yaml
