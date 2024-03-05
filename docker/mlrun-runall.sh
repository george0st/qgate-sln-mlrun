#!/bin/sh

# Create and run all docker containers

# mysql
docker run --name mlrun-mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=jist -e MYSQL_DATABASE=test -e MYSQL_USER=testuser -e MYSQL_PASSWORD=testpwd -d mysql:8.3 --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci

# postgres
docker run --name mlrun-postgres -p 5432:5432 -e POSTGRES_DB=test -e POSTGRES_USER=testuser -e POSTGRES_PASSWORD=testpwd -d postgres:16

# redis
docker run --name mlrun-redis -p 6379:6379 -m 512m -d redis:7.2
