#!/bin/sh

# Hack for local installation see https://github.com/mlrun/mlrun/blob/development/hack/local/README.md

SHARED_DIR=~/mlrun-data

docker pull mlrun/jupyter:1.7.0
docker pull mlrun/mlrun-ui:1.7.0

docker network create mlrun-network
docker run -it -p 8080:8080 -p 8888:8888 --rm -d --network mlrun-network --name jupyter -v ${SHARED_DIR}:/home/jovyan/data mlrun/jupyter:1.7.0
docker run -it -p 4000:80 --rm -d --network mlrun-network --name mlrun-ui -e MLRUN_API_PROXY_URL=http://jupyter:8080 mlrun/mlrun-ui:1.7.0

# or standard installation on Kubernates in Docker
# TBD.