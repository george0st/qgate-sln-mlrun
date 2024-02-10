#!/bin/sh

docker pull mysql:8.3
docker run --name mlrun-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=jist -e MYSQL_DATABASE=test -e MYSQL_USER=test -e MYSQL_PASSWORD=test -d mysql:8.3 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci