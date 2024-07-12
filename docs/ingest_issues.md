# Ingest issue 

List of extra situations/exceptions during feature set ingest with relation to the 
source, target, setting for InferOption.default() or InferOption.Null.

BTW: in case of InferOption.default(), the data types are defined based on discovery during
the preview (it is operation before the own ingest).

Experience from these test cases:
 - TS202-205
 - TS303-305
 - TS404-405

## ParquetTarget

 Target | Source            | InferOptions.default()                                                                                                                | InferOptions.Null | 
--------|-------------------|---------------------------------------------------------------------------------------------------------------------------------------|--------|
Parquet | TSx02: DataFrame  | Ok                                                                                                                                    | Ok
Parquet | TSx03: CSV        | Ok                                                                                                                                    | Ok
Parquet | TSx04: Parquet    | ArrowTypeError: ("Expected bytes, got a 'datetime.date' object", 'Conversion failed for column party-establishment with type object') | Ok 
Parquet | TSx05: SQL(MySQL) | Ok                                                                                                                                    | Ok


## RedisTarget

 Target | Source             | InferOptions.default() | InferOptions.Null  | 
--------|--------------------|------------------------|--------------------|
Redis   | TSx02: DataFrame   | ??                     | ??                 
Redis   | TSx03: CSV         | ??                     | ??                 
Redis   | TSx04: Parquet     | Ok                     | ??                 
Redis   | TSx05: SQL(MySQL)  | ??                     | ??                 

TBD.