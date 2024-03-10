# Kafka as on-line source

## 1. Preconditions for OS Windows

 - Install Desktop Docker, [see](./desktopdocker.md)

## 2. Run Kafka (in container, focus on conduktor solution)
 - https://github.com/conduktor/kafka-stack-docker-compose/blob/master/zk-single-kafka-single.yml
 - `docker-compose -f zk-single-kafka-single.yml up -d`

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
