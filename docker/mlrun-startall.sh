#!/bin/sh

# Start all existing containers

# mysql
docker start mlrun-mysql

# postgres
docker start mlrun-postgres

# redis
docker start mlrun-redis

# kafka
docker start zoo1
docker start kafka1