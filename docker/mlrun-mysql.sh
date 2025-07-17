#!/bin/sh

docker pull mysql:9.3.0
docker run --name mlrun-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=jist -e MYSQL_DATABASE=test -e MYSQL_USER=testuser -e MYSQL_PASSWORD=testpwd -d mysql:9.3.0 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci