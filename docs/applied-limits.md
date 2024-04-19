# Applied limits for MLRun Quality Gate

## MLRun Client
1. The MLRun Client (in version >= 1.5.2) **does not support OS Windows**, 
see [ML-4907](https://docs.mlrun.org/en/latest/change-log/index.html#limitations). Know issues:
   - mistake in datatime conversion under python 3.9 and OS Windows,
   see [issue](https://stackoverflow.com/questions/77743056/python-oserror-errno-22-invalid-argument-for-datetime-timestamp)
   and [RedisNoSqlTarget - OSError: [Errno 22] Invalid argument](https://github.com/mlrun/mlrun/issues/4845)
   - it is necessary to use Linux path (not Windows path) for some cases
   e.g. for [CSVTarget](https://github.com/mlrun/mlrun/issues/5056)
   - missing MLRun tests under OS Windows
   - probably others (without full tracking and addition details)

NOTE: Solution, it is necessity to use WSL2 under OS Windows

## Feature Vector
1. The data read (via feature vector) **accept only ONE on-line and
   one off-line target** in FeatureSet, see [Slack discussion](https://mlopslive.slack.com/archives/C014XCMNY4Q/p1701025414893399?thread_ts=1701021926.280329&cid=C014XCMNY4Q)
   - in case of e.g. more on-line targets, it is not possible to choose 
   relevant target for FeatureVector  

## RedisNoSqlTarget

1. Issue with support **date** type
   - see [combination of RedisNoSqlTarget and ParquetSource](https://github.com/mlrun/mlrun/issues/5447)


## SQLTarget

NOTE: It is in preview version, very limited with focus on MySQL only, 
see detail below

1. SQLTarget limits
   - missing support MORE primary keys (only ONE primary key is supported right now)
   - schema for mapping FeatureStore to Table must be defined manually (not automatically)
   - see detail https://github.com/mlrun/mlrun/issues/5051

2. SqlTarget is limited to MySql, if you need to create table (SqlTarget is in
  Technical Preview)
    - see the detail https://github.com/mlrun/mlrun/issues/5231
    - NOTE: It is possible to use work-arround, create table before the ingest

3. SqlTarget issue with save/load content mapping for SqlTarget
   - see the detail https://github.com/mlrun/mlrun/issues/5238

## KafkaTarget

1. It is not possible to use feature vector operations in KafkaTarget
   - but it is possible to do ingest to the KafkaTarget or consume data from 
   KafkaSource (with triggers)
   - it means, test scenarios TS401, TS501, TS502, TS601 and TS701 for
   KafkaTarget was switch-off
   - the scenario switch-off was realised based on change of in '*-agate-kafka.json', 
   see the path './qgate-sln-mlrun/model_changes/*'
   

## CSVSource

1. CSVSource supports only default CSV setting, it means sep=',', decimal='.' and 
   with na_filter=True (it is the issue for nan value or empty strings) 
   - in case of different setting, it is better to use Pandas/DataFrame source
     (it has bigger variability)

## Others
1. Not to use the engine `pandas`
   - this `pandas` engine is useful only for test purpose (see the first 
   info about that in change log for MLRun version 1.6.0)
