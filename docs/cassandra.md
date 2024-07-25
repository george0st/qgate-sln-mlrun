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
   - or create container with name 'mlrun-redis', use image 'redis:latest' and open ports 6379:6379
     - `docker run --name mlrun-cassandra -p 9042:9042 -d redis:cassandra`

3. Test Cassandra in container
   - interactive access to the container
     - `docker exec -it mlrun-cassandra cqlsh`
   - show keyspaces (databases)
     - `SELECT * FROM system_schema.keyspaces;`
   - create keyspace `test`
     - `CREATE KEYSPACE IF NOT EXISTS test WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1};`
   - choose keyspace `test`
     - `USE test;`
   - create table 'tbl'
     - `CREATE TABLE IF NOT EXISTS test.tbl (fn0 int, fn1 text, fn2 text, PRIMARY KEY (fn0, fn1));`
   - insert data
     - `INSERT INTO test.tbl (fn0, fn1, fn2) VALUES(1,'tiger', 'scott');`
     - `INSERT INTO test.tbl (fn0, fn1, fn2) VALUES(2,'john', 'novak');`
   - select data
     - 

## 3. Use Cassandra for tests

   - TBD.