# Configuration


## Path to data storage
Path to the output directory for **off-line storage** (valid for target 'parquet', 'csv', etc.)
  - local file system `QGATE_OUTPUT = ./output/`
  - object storage `QGATE_OUTPUT = TBD`

## Redis
Setup of Redis for **on-line FeatureStore** (valid fot target 'redis')
  - `QGATE_REDIS = redis://localhost:6379`
  - detail description, see [Redis](./redis.md)
