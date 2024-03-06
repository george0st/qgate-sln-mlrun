# Configuration

The view to setting of test configuration.

## 1. Model definition
The path to the QGate model definition (the path can be relative or full) e.g. ../qgate-model
  - `QGATE_DEFINITION = ../qgate-model`

## 2. Data set
The name of data set for testing e.g. "01-size-100", "02-size-1K", etc.
  - `QGATE_DATASET = 01-size-100`

## 3. Filter projects
The list of projects for testing e.g. agate-1, agate-2, etc. 
Default is empty list (all projects will be tested)
  - `QGATE_FILTER_PROJECTS = agate-2`

## 4. Output
The path to the output directory for **off-line storage** (valid for target 'parquet', 'csv', etc.)
  - local file system `QGATE_OUTPUT = ./output`
  - object storage `QGATE_OUTPUT = TBD`

## 5. Redis
The setup of Redis for **on-line source/target** (valid fot target 'redis')
  - `QGATE_REDIS = redis://localhost:6379`
  - detail description, see [Redis](./redis.md)

## 6. MySQL
The setup of MySQL for **on-line source/target** (valid fot target 'mysql')
  - `QGATE_MYSQL = mysql+pymysql://testuser:testpwd@localhost:3306/test`
  - detail description, see [MySQL](./mysql.md)

## 7. Postgres
The setup of Postgres for **on-line source/target** (valid fot target 'postgres')
  - `QGATE_POSTGRESL = postgresql+psycopg2://testuser:testpwd@localhost:5432/test`
  - detail description, see [Postgres](./postgres.md)

NOTE: limited usage based on SqlTarget technical preview state
    (the main focus on MySQL)

## 8. Kafka
TBD. see helper https://hackernoon.com/setting-up-kafka-on-docker-for-local-development
https://hub.docker.com/r/confluentinc/cp-kafka

