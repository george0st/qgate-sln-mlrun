#!/bin/sh

# Create and run all docker containers

# mysql
./mlrun-mysql.sh

# postgres
./mlrun-postgres.sh

# redis
./mlrun-redis.sh

# cassandra
./mlrun-cassandra.sh

# scylla
#./mlrun-scylla.sh

# kafka
./mlrun-kafka.sh

