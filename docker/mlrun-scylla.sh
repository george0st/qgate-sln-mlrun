#!/bin/sh

docker pull scylladb/scylla:5.4
docker run --name mlrun-scylladb -p 9042:9042 -d scylladb/scylla:5.4
