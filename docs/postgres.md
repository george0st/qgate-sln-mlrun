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

3. Test Postgres in container
   - interactive access to the container
     - `docker exec -it mlrun-postgres psql -U testuser test`
   - list of users and their roles
     - `test=# \du` 
   - show list of databases
     - `test=# \l`
   - list of DB tables
     - `test=# \dt`
   - switch to database `postgres`
     - `test=# \c postgres`
   - more commands [see](https://hasura.io/blog/top-psql-commands-and-flags-you-need-to-know-postgresql/)
     
## 3. Use Postgres for tests
 - Update `qgate-sln-mlrun.env`, change setting for `QGATE_POSTGRES`
   - format `QGATE_POSTGRES = postgresql+pg8000://<username>:<password>@<host>:<port>/<db_name>`
   - see `QGATE_POSTGRES = postgresql+pg8000://testuser:testpwd@localhost:5432/test`
postgresql+pyscopg2
   - postgresql+psycopg2
   - postgresql+psycopg
 - NOTE:
   - https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg2
   - https://pypi.org/project/psycopg2/

## 4. Install these python packages
    TBD.