#!/bin/sh

# single kafka with singl zookeeper
# NOTE: YAML file was tailor based on original source
# see https://github.com/conduktor/kafka-stack-docker-compose/blob/master/zk-single-kafka-single.yml

docker-compose -f ./config/zk-single-kafka-single.yml up -d
