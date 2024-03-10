#!/bin/sh

# single kafka with singl zookeeper
docker-compose -f ./config/zk-single-kafka-single.yml up -d
