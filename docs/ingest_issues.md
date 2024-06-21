# Ingest issue 

List of extra situations/exceptions during feature set ingest with relation to the 
source, target, setting for InferOption.default() or InferOption.Null.

BTW: in case of InferOption.default(), the data types are defined based on discovery during
the preview (it is operation before the own ingest).

## ParquetTarget

Experinece from TS301-305, TS401-405

 Target | Source     | InferOptions.default()                                                                                                                | InferOptions.Null | 
--------|------------|---------------------------------------------------------------------------------------------------------------------------------------|--------|
Parquet | DataFrame  | Ok                                                                                                                                    | Ok
Parquet | CSV        | Ok                                                                                                                                    | Ok
Parquet | Parquet    | ArrowTypeError: ("Expected bytes, got a 'datetime.date' object", 'Conversion failed for column party-establishment with type object') | Ok 
Parquet | SQL(MySQL) | Ok                                                                                                                                    | Ok


## RedisTarget

 Target | Source     | InferOptions.default()                                                                                                                | InferOptions.Null | 
--------|------------|---------------------------------------------------------------------------------------------------------------------------------------|--------|
Redis   | Parquet    | Ok                                                                                                                                    | ??

TBD.