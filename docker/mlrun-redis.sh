#!/bin/sh

docker pull redis:7.2
docker run --name mlrun-redis -p 6379:6379 -m 512m -d redis:7.2