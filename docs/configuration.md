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
The setup of Redis for **on-line source/target** (valid for target 'redis')
  - `QGATE_REDIS = redis://localhost:6379`
  - detail description, see [Redis](./redis.md)

## 6. MySQL
The setup of MySQL for **on-line source/target** (valid for target 'mysql')
  - `QGATE_MYSQL = mysql+pymysql://testuser:testpwd@localhost:3306/test`
  - detail description, see [MySQL](./mysql.md)

## 7. Postgres
The setup of Postgres for **on-line source/target** (valid for target 'postgres')
  - `QGATE_POSTGRES = postgresql+psycopg2://testuser:testpwd@localhost:5432/test`
  - detail description, see [Postgres](./postgres.md)
  - NOTE: limited usage based on SqlTarget technical preview state
    (the main focus on MySQL)

## 8. Kafka
The setup of Kafka for **on-line source** (valid for target 'kafka')
  - `QGATE_KAFKA = localhost:9092, testtopic`
  - detail description, see [Kafka](./kafka.md)

## Supported sources and targers in MLRun
 - [Sources-Targets from MLRun](https://docs.mlrun.org/en/latest/feature-store/sources-targets.html)