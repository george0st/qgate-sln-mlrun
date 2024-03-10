# Kafka as on-line source

## 1. Preconditions for OS Windows

 - Install Desktop Docker, [see](./desktopdocker.md)

## 2. Run Kafka (in container, focus on conduktor solution)

1. Install kafka and zookeeper as docker-compose
 - run `./docker/mlrun-kafka.sh`
 - or run `docker-compose -f zk-single-kafka-single.yml up -d`
 - Note:
   - YAML file is based on [Conduktor YAML file](https://github.com/conduktor/kafka-stack-docker-compose/blob/master/zk-single-kafka-single.yml)

2. Test Kafka in container

 - interactive access to the container
   - `docker exec -it kafka1 /bin/bash`
   - get kafka version `kafka-topics --version`


## Useful sources

1. Conduktor & Kafka
 - see https://www.conduktor.io/kafka/how-to-start-kafka-using-docker/

2. Installation steps
 - https://www.linkedin.com/pulse/local-kafka-setup-using-docker-sandeep-khurana/
 - see YAML file
    - https://github.com/bitnami/containers/blob/main/bitnami/kafka/docker-compose.yml

3. Others
 - helper, see https://hackernoon.com/setting-up-kafka-on-docker-for-local-development
 - docker image, see https://hub.docker.com/r/confluentinc/cp-kafka
 - quick start, see https://docs.confluent.io/platform/current/platform-quickstart.html#ce-docker-quickstart
