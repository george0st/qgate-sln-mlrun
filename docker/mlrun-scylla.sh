#!/bin/sh

docker pull scylladb/scylla:2025.1.1
docker run --name mlrun-scylladb -p 9042:9042 -p 7199:7199 -d scylladb/scylla:2025.1.1
