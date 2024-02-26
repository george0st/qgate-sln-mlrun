# Postgres as on-line source/target

## 1. Preconditions for OS Windows

 - Install Desktop Docker, [see](./desktopdocker.md)

## 2. Run Postgres (in container)

1. Get image from official source
   - get specific postgres image version 16 `docker pull postgres:16`
   - or get last redis image `docker pull postgres:latest`
   - Note
     - available [versions](https://hub.docker.com/_/postgres)/[tags](https://hub.docker.com/_/postgres/tags)
