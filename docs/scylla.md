# Scylla as on-line source/target

## 1. Preconditions for OS Windows

 - Install Desktop Docker, [see](./desktopdocker.md)

## 2. Run Scylla (in container)

1. Get image from official source
   - get specific scylla image version 6.2.0 `docker pull scylladb/scylla:6.2.0`
   - or get last scylla image `docker pull scylladb/scylla:latest`
   - Note
     - available [versions](https://hub.docker.com/r/scylladb/scylla)/[tags](https://hub.docker.com/r/scylladb/scylla/tags)

2. Run new container
   - create container with name 'mlrun-scylla', use image 'scylladb/scylla:6.2.0' and open ports 9042:9042
     - `docker run --name mlrun-scylla -p 9042:9042 -p 7199:7199 -d scylladb/scylla:6.2.0`
   - or create container with name 'mlrun-scylla', use image 'scylladb/scylla:latest' and open ports 9042:9042
     - `docker run --name mlrun-scylla -p 9042:9042 -p 7199:7199 -d scylladb/scylla:latest`
   - NOTE:
     - **port 9042** is used from scylla listener
     - **port 7199** is using from admin tools such as `nodetool`, etc.
     
3. Test Scylla in container
   - interactive access to the container
     - `docker exec -it mlrun-scylla cqlsh`
     - or `docker exec -it mlrun-scylla bash`
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
   - insert data with TTL 2 days (172.800 seconds, note - max TTL value can be 20 years)
     - `INSERT INTO test.tbl (fn0, fn1, fn2) VALUES(1,'tiger', 'scott') USING TTL 172800;`
     - `INSERT INTO test.tbl (fn0, fn1, fn2) VALUES(2,'john', 'novak') USING TTL 172800;`
   - select data with indexed column in WHERE 
     - `SELECT * FROM test.tbl WHERE fn0=1;`
   - select data without indexed column in WHERE (allow filtering as low/bad query performance)
     - `SELECT * FROM test.tbl WHERE fn2='novak' ALLOW FILTERING;`


## 3. Use Scylla for tests

   - TBD.