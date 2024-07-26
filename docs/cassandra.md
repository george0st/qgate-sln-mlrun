# Cassandra as on-line source/target

## 1. Preconditions for OS Windows

 - Install Desktop Docker, [see](./desktopdocker.md)

## 2. Run Cassandra (in container)

1. Get image from official source
   - get specific cassandra image version 5.0-rc1 `docker pull cassandra:5.0-rc1`
   - or get last cassandra image `docker pull cassandra:latest`
   - Note
     - available [versions](https://hub.docker.com/_/cassandra)/[tags](https://hub.docker.com/_/cassandra/tags)

2. Run new container
   - create container with name 'mlrun-cassandra', use image 'cassandra:5.0-rc1' and open ports 9042:9042
     - `docker run --name mlrun-cassandra -p 9042:9042 -d cassandra:5.0-rc1`
   - or create container with name 'mlrun-cassandra', use image 'cassandra:latest' and open ports 9042:9042
     - `docker run --name mlrun-cassandra -p 9042:9042 -d cassandra:latest`

3. Test Cassandra in container
   - interactive access to the container
     - `docker exec -it mlrun-cassandra cqlsh`
   - show keyspaces (databases)
     - `DESCRIBE KEYSPACES;`
     - or `SELECT * FROM system_schema.keyspaces;`
   - create keyspace `test`
     - `CREATE KEYSPACE IF NOT EXISTS test WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};`
   - describe detail about keyspace
     - `DESCRIBE KEYSPACE test;`
   - choose keyspace `test`
     - `USE test;`
   - show tables (in current keyspace)
     - `DESCRIBE TABLES;` 
   - create table 'tbl'
     - `CREATE TABLE IF NOT EXISTS test.tbl (fn0 int, fn1 text, fn2 text, PRIMARY KEY (fn0, fn1));`
   - describe table (full information about table structure and setting)
     - `DESCRIBE TABLE test.tbl;`
   - insert data with TTL 2 days (172800 seconds)
     - `INSERT INTO test.tbl (fn0, fn1, fn2) VALUES(1,'tiger', 'scott') USING TTL 172800;`
     - `INSERT INTO test.tbl (fn0, fn1, fn2) VALUES(2,'john', 'novak')  USING TTL 172800;`
   - select data
     - `SELECT * FROM test.tbl WHERE fn0=1;`
     - `SELECT * FROM test.tbl WHERE fn2='novak' ALLOW FILTERING;`


## 3. Use Cassandra for tests

   - TBD.