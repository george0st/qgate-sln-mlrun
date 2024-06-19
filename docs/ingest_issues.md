# Ingest issue 

List of extra situations/exceptions during feature set ingest with relation to the 
source, target, setting for InferOption.default() or InferOption.Null.

BTW: in case of InferOption.default(), the data types are defined based on discovery during
the preview (it is operation before the own ingest).

 Target | Source  | InferOptions.default()                                                                                                                | InferOptions.Null | 
--------|---------|---------------------------------------------------------------------------------------------------------------------------------------|-------------------|
Parquet | Parquet | ArrowTypeError: ("Expected bytes, got a 'datetime.date' object", 'Conversion failed for column party-establishment with type object') | Ok 
Parquet | CSV     | Ok                                                                                                                                    | Ok                                                                                                                                    
Redis   | Parquet | Ok                                                                                                                                    | ??


TBD.