#!/bin/sh

docker pull redis:7.2
docker run --name mlrun-redis -p 6379:6379 -d redis:7.2