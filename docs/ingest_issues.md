# Ingest issue 

List of extra situations/exceptions during feature set ingest with relation to the 
source, target and other ingest conditions.


 Target | Source  | InferOptions.default()                                                                                                                | InferOptions.Null | 
--------|---------|---------------------------------------------------------------------------------------------------------------------------------------|-------------------|
Parquet | Parquet | ArrowTypeError: ("Expected bytes, got a 'datetime.date' object", 'Conversion failed for column party-establishment with type object') | Ok 
Parquet | CSV     | Ok                                                                                                                                    | ??                                                                                                                                    
Redis   | Parquet | ??                                                                                                                                    | ??


TBD.