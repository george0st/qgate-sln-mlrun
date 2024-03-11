#!/bin/sh

# MLRun in docker composer

# NOTE:
#   - YAML file was tailor based on original source
#   - see https://github.com/mlrun/mlrun/blob/development/docs/install/compose.yaml
#   - or https://docs.mlrun.org/en/latest/install/local-docker.html#use-mlrun-with-your-own-client

# $Env:HOST_IP=<your host IP address>
# $Env:HOST_IP=192.168.0.150
$Env:HOST_IP=10.130.175.252
$Env:SHARED_DIR="c:/Apps/mlrun-data"
mkdir $Env:SHARED_DIR
docker-compose -f ./config/compose.yaml up -d
