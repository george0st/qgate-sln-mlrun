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
 - list kafka topics
   - `kafka-topics --bootstrap-server localhost:9092 --list`
   - or `docker exec -t kafka1 /usr/bin/kafka-topics --bootstrap-server localhost:9092 --list`
 - create (define) new kafka topic 'aa'
   - `kafka-topics --bootstrap-server localhost:9092 --topic aa --create --partitions 3 --replication-factor 1`
   - or `docker exec -t kafka1 /usr/bin/kafka-topics --bootstrap-server localhost:9092 --topic aa --create --partitions 3 --replication-factor 1`
 - fire (produce) new kafka topic 'aa' (CTRL+C for finish new topic)
   - `kafka-console-producer --bootstrap-server localhost:9092 --topic aa`
   - or `docker exec -t kafka1 /usr/bin/kafka-console-producer --bootstrap-server localhost:9092 --topic aa`
 - get (consume) kafka topics 'aa'
   - `kafka-console-consumer --bootstrap-server localhost:9092 --topic aa --from-beginning`
   - or `docker exec -t kafka1 /usr/bin/kafka-console-consumer --bootstrap-server localhost:9092 --topic aa --from-beginning`


## 3. Use Kafka for tests

 - Update `qgate-sln-mlrun.env`, change setting for `QGATE_KAFKA`
   - format `QGATE_KAFKA = <url>, <topic name>`
   - see `QGATE_KAFKA = localhost:9092, testtopic`

## 4. Install these python packages

 - SQLAlchemy based on MLRun extras see `pip install mlrun[kafka]` or [dependencies.py in MLRun](https://github.com/mlrun/mlrun/blob/development/dependencies.py)
   - it required `pip install kafka-python~=2.0`
   - it required `pip install avro~=1.11`
 - NOTE
   - it is valid for MLRun 1.6.2

## Useful sources for kafka

1. Conduktor & Kafka
 - see https://www.conduktor.io/kafka/how-to-start-kafka-using-docker/

2. Others
 - other YAML file, see https://github.com/bitnami/containers/blob/main/bitnami/kafka/docker-compose.yml
 - helper, see https://hackernoon.com/setting-up-kafka-on-docker-for-local-development
 - docker image, see https://hub.docker.com/r/confluentinc/cp-kafka
 - quick start, see https://docs.confluent.io/platform/current/platform-quickstart.html#ce-docker-quickstart
