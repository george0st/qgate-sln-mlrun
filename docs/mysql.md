# MySQL as on-line source/target

## 1. Preconditions for OS Windows

 - Install Desktop Docker, [see](./desktopdocker.md)

## 2. Run MySQL (in container)

1. Get image from official source
   - get specific redis image version 8.3 `docker pull mysql:8.3`
   - or get last redis image `docker pull mysql:latest`
   - Note
     - available [versions](https://hub.docker.com/_/mysql)/[tags](https://hub.docker.com/_/mysql/tags)

2. Run new container
   - create container with name 'mlrun-mysql', use image 'mysql:8.3' and open ports 3306:3306
     - `docker run --name mlrun-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=jist -e MYSQL_DATABASE=test -e MYSQL_USER=testuser -e MYSQL_PASSWORD=testpwd -d mysql:8.3 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci`
   - or create container with name 'mlrun-mysql', use image 'mysql:latest' and open ports 3306:3306
     - `docker run --name mlrun-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=jist -e MYSQL_DATABASE=test -e MYSQL_USER=testuser -e MYSQL_PASSWORD=testpwd -d mysql:last --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci`
   - NOTE:
     - user `testuser`, password `testpwd`

3. Test MySQL in container
   - interactive access to the container
     - `docker exec -it mlrun-mysql bash`
   - login to mysql under the user 'root'
     - `mysql -u root -p` and password `jist`
   - show list of users
     - `SELECT user FROM mysql.user;`
   - show list of databases
     - `show databases;`
   - switch to use database `test`
     - `use test;`
   - show list of tables
     - `show tables;`

## 3. Use MySQL for tests

 - Update `qgate-sln-mlrun.env`, change setting for `QGATE_MYSQL`
   - format `QGATE_MYSQL = mysql+<dialect>://<username>:<password>@<host>:<port>/<db_name>`
   - see `QGATE_MYSQL = mysql+pymysql://testuser:testpwd@localhost:3306/test`
 - Note
   - List of [Dialects](https://docs.sqlalchemy.org/en/20/dialects/index.html)

## 4. Install these python packages

 - SQLAlchemy based on MLRun extras see `pip install mlrun[sqlalchemy]` or [dependencies.py in MLRun](https://github.com/mlrun/mlrun/blob/development/dependencies.py)
   - it required `pip install sqlalchemy~=1.4`
 - Dialect pymysql
   - it required `pip install pymysql~=1.1`
 - Cryptography support
   - it required `pip install cryptography~=42.0`
 - NOTE
   - these are versions valid for MLRun 1.5.2

