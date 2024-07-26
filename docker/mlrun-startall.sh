#!/bin/sh

# Start all existing containers

# mysql
docker start mlrun-mysql

# postgres
docker start mlrun-postgres

# redis
docker start mlrun-redis

# cassandra
docker start mlrun-cassandra

# scylla
#docker start mlrun-scylla

# kafka
docker start zoo1
docker start kafka1

