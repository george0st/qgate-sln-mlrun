# MySQL as on-line feature store

## 1. Preconditions for OS Windows

1. Installed **Docker Desktop with WSL 2**
2. You can test success installation
   - check Docker Desktop, cmd `docker --version`
   - check WSL2, cmd `wsl --status` (expected info 'Default Version: 2')
   - check installed distributions, cmd `wsl -l` (expected info 'docker-desktop' and 'docker-desktop-data')

## 2. Run MySQL (in container)

1. Get image from official source
   - get specific redis image version 7.2 `docker pull mysql:8.3`
   - or get last redis image `docker pull mysql:latest`
   - Note
     - available [versions](https://hub.docker.com/_/mysql)/[tags](https://hub.docker.com/_/mysql/tags)

2. Run new container
   - create container with name 'mlrun-mysql', use image 'mysql:8.3' and open ports 8081:8080
     - `docker run --name mlrun-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=jist -e MYSQL_DATABASE=test -e MYSQL_USER=jist -e MYSQL_PASSWORD=jist -d mysql:8.3 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci`
   - or create container with name 'mlrun-mysql', use image 'mysql:latest' and open ports 8081:8080
     - `docker run --name mlrun-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=jist -e MYSQL_DATABASE=test -e MYSQL_USER=jist -e MYSQL_PASSWORD=jist -d mysql:last --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci`
   - NOTE:
     - user `jist`, password `jist`

3. Test MySQL in container
   - interactive access to the container
     - `docker exec -it mlrun-mysql bash`
   - login to mysql under the user 'root'
     - `mysql -u root -p` and password `jist`
   - show list of users
     - `SELECT user FROM mysql.user;`
   - show list of databases
     - `show databases;`

## 3. Use MySQL for tests

 - Update `qgate-sln-mlrun.env`, change setting for `QGATE_MYSQL`
   - see `QGATE_MYSQL = http://localhost:8081`

