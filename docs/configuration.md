# Configuration

The view to setting of test configuration.

## 1. Host IP (optional)
The IP address for installation of MLRun. This env. variable can be used such as ${HOST_IP} 
in other variables in env. file. It is important to use not `localhost`, but relevant
IP address, because the services in pod/node need to have access to valid end point
of the services (such as redis, kafka, etc.).
 - `HOST_IP = 192.168.0.150`

## 2. Check Host IP (optional)
The check host IP, will check of HOST_IP based on compare with IP for network adapter
(the network adapter is identified based on the name or the name prefix). In case of 
differences, it will generate warning during the run. The valid values are e.g. "wi-fi"
or "wi" or "WI" (value is case-insensitive)  
 - `HOST_IP_CHECK = "wi-fi"`

## 3. Anonym mode (optional)
The switch for setup `On` or `Off` anonym mode (default is `Off`). If anonym mode is `On` than 
the output file names in directory `QGATE_OUTPUT` are only with date information
(without the time detail for file creation). The host variable `Host` in output file 
contains static information `Anonym/192.168.0.1` (not real host name and IP address).
 - `QGATE_ANONYM_MODE = On`

## 4. Model definition
The path to the [QGate model](https://github.com/george0st/qgate-model) definition (the path
can be relative or full) e.g. ../qgate-model
  - `QGATE_DEFINITION = ../qgate-model`

## 5. Data set
The name of data set (as directory name in model definition) for testing e.g. "01-size-100", "02-size-1K", etc.
The directory contains CSV/GZ and Parquet files.
  - `QGATE_DATASET = 01-size-100`

## 6. Filter projects
The list of projects for testing e.g. agate-1, agate-2, etc. 
Default is empty list (all projects will be tested)
  - `QGATE_FILTER_PROJECTS = agate-2, agate-redis-parquet`

## 7. Filter scenarios (optional)
The list of test scenarios for testing e.g. TS201, etc. (it is 
important to keep and know TS dependencies). Default is empty list (all test
scenarios will be tested)
  - `QGATE_FILTER_SCENARIOS = TS101, TS102, TS205`

## 8. Output
The path to the output directory for **off-line storage** (valid for target 'parquet', 'csv', etc.)
  - local file system `QGATE_OUTPUT = ./output`
  - object storage `QGATE_OUTPUT = TBD.`

## 9. Redis (optional)
The setup of Redis for **on-line source/target** (valid for target 'redis')
  - `QGATE_REDIS = redis://${HOST_IP}:6379`
  - detail description, see [Redis](./redis.md)

## 10. MySQL (optional)
The setup of MySQL for **on-line source/target** (valid for target 'mysql')
  - `QGATE_MYSQL = mysql+pymysql://testuser:testpwd@${HOST_IP}:3306/test`
  - detail description, see [MySQL](./mysql.md)

## 11. Postgres (optional)
The setup of Postgres for **on-line source/target** (valid for target 'postgres')
  - `QGATE_POSTGRES = postgresql+psycopg2://testuser:testpwd@${HOST_IP}:5432/test`
  - detail description, see [Postgres](./postgres.md)
  - NOTE: limited usage based on SqlTarget technical preview state
    (the main focus on MySQL)

## 12. Kafka (optional)
The setup of Kafka for **on-line source** (valid for target 'kafka')
  - `QGATE_KAFKA = ${HOST_IP}:9092`
  - detail description, see [Kafka](./kafka.md)

## NOTES
 - [MLRun configuration](config_in_docker.md) include IP addresses for Target/Source
 - Supported [sources and targers](https://docs.mlrun.org/en/latest/feature-store/sources-targets.html) in MLRun
