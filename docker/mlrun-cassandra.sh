#!/bin/sh

docker pull cassandra:5.0.1
docker run --name mlrun-cassandra -p 9042:9042 -p 7199:7199 -d cassandra:5.0.1
