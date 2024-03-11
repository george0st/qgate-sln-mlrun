#!/bin/sh

# Create and run all docker containers

# mysql
./mlrun-mysql.sh

# postgres
./mlrun-postgres.sh

# redis
./mrlun-redis.sh

# kafka
