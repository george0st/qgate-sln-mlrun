# Configuration


## 1. Model definition
The Path to the QGate model definition (the path can be relative or full) e.g. ../qgate-model/
  - `QGATE_DEFINITION = ../qgate-model/`

## 2. Data set
The name of data set for testing e.g. "01-size-100", "02-size-1K", etc.
  - `QGATE_DATASET = 01-size-100`

## 3. Output
The path to the output directory for **off-line storage** (valid for target 'parquet', 'csv', etc.)
  - local file system `QGATE_OUTPUT = ./output/`
  - object storage `QGATE_OUTPUT = TBD`

## 4. Redis
The setup of Redis for **on-line FeatureStore** (valid fot target 'redis')
  - `QGATE_REDIS = redis://localhost:6379`
  - detail description, see [Redis](./redis.md)

## 5. MySQL
The setup of MySQL for **on-line FeatureStore** (valid fot target 'mysql')
  - `QGATE_MYSQL = http://localhost:8081`
  - detail description, see [MySQL](./mysql.md)