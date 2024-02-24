#!/bin/sh

docker pull postgres:12.18
docker run --name mlrun-postgres -p 8010:8080 -e POSTGRES_PASSWORD=testpwd -d postgres:12.18