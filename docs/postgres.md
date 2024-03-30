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
   - create table `my_table`
     - `CREATE TABLE my_table(id int, description varchar(50));`
   - more commands [see](https://hasura.io/blog/top-psql-commands-and-flags-you-need-to-know-postgresql/)
     
## 3. Use Postgres for tests
 - Update `qgate-sln-mlrun.env`, change setting for `QGATE_POSTGRES`
   - format `QGATE_POSTGRES = postgresql+<dialect>://<username>:<password>@<host>:<port>/<db_name>`
   - see `QGATE_POSTGRES = postgresql+psycopg://testuser:testpwd@localhost:5432/test`
   - or see `QGATE_POSTGRES = postgresql+psycopg2://testuser:testpwd@localhost:5432/test`
 - NOTE:
   - [SQLAlchemy postgres](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html)
   - [Dialect psycopg](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html#module-sqlalchemy.dialects.postgresql.psycopg)
   - [Pypi psycopg](https://pypi.org/project/psycopg/)

## 4. Install these python packages
 - SQLAlchemy based on MLRun extras see `pip install mlrun[sqlalchemy]` or [dependencies.py in MLRun](https://github.com/mlrun/mlrun/blob/development/dependencies.py)
   - it required `pip install sqlalchemy~=1.4`
 - Dialect psycopg or psycopg2 
   - it required `pip install psycopg~=3.1` or `pip install psycopg2~=2.9`
 - Cryptography support
   - it required `pip install cryptography~=42.0`
 - NOTE
   - these are versions valid for MLRun 1.6.2
