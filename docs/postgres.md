# Postgres as on-line source/target

## 1. Preconditions for OS Windows

 - Install Desktop Docker, [see](./desktopdocker.md)

## 2. Run Postgres (in container)

1. Get image from official source
   - get specific postgres image version 16 `docker pull postgres:16`
   - or get last redis image `docker pull postgres:latest`
   - Note
     - available [versions](https://hub.docker.com/_/postgres)/[tags](https://hub.docker.com/_/postgres/tags)

2. Run new container
   - create container with name 'mlrun-postgres', use image 'postgres:16' and open ports 5432:5432
     - `docker run --name mlrun-postgres -p 5432:5432 -e POSTGRES_DB=test -e POSTGRES_USER=testuser -e POSTGRES_PASSWORD=testpwd -d postgres:16`
   - or create container with name 'mlrun-mysql', use image 'postgres:16' and open ports 5432:5432
     - `docker run --name mlrun-postgres -p 5432:5432 -e POSTGRES_DB=test -e POSTGRES_USER=testuser -e POSTGRES_PASSWORD=testpwd -d postgres:last`
   - NOTE:
     - user `testuser`, password `testpwd`