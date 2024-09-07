#!/bin/sh

docker pull scylladb/scylla:6.1.1
docker run --name mlrun-scylladb -p 9042:9042 -d scylladb/scylla:6.1.1
