# Cassandra as on-line source/target

## 1. Preconditions for OS Windows

 - Install Desktop Docker, [see](./desktopdocker.md)

## 2. Run Cassandra (in container)

1. Get image from official source
   - get specific cassandra image version 5.0.4 `docker pull cassandra:5.0.4`
   - or get last cassandra image `docker pull cassandra:latest`
   - Note
     - available [versions](https://hub.docker.com/_/cassandra)/[tags](https://hub.docker.com/_/cassandra/tags)
     - github for [cassandra image](https://github.com/docker-library/cassandra/blob/master/5.0/Dockerfile)
     - main image setting
       - ENV **CASSANDRA_HOME** /opt/cassandra 
       - ENV **CASSANDRA_CONF** /etc/cassandra 
       - ENV PATH $CASSANDRA_HOME/bin:$PATH 
       - VOLUME **/var/lib/cassandra**
       - and key configuration
         - **CASSANDRA_CONF/cassandra.yaml**
         - **CASSANDRA_CONF/cassandra-rackdc.properties**

2. Run new container
   - create container with name 'mlrun-cassandra', use image 'cassandra:5.0.4' and open ports 9042:9042
     - `docker run --name mlrun-cassandra -p 9042:9042 -p 7199:7199 -d cassandra:5.0.4`
   - or create container with name 'mlrun-cassandra', use image 'cassandra:latest' and open ports 9042:9042
     - `docker run --name mlrun-cassandra -p 9042:9042 -p 7199:7199 -d cassandra:latest`
   - NOTE:
     - **port 9042** is used from cassandra listener
     - **port 7199** is using from admin tools such as `nodetool`, etc.

3. Test Cassandra in container
   - interactive access to the container
     - `docker exec -it mlrun-cassandra cqlsh` 
     - or `docker exec -it mlrun-cassandra bash`
     - or `docker exec -it mlrun-cassandra sh`
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


## 3. Use Cassandra for tests

   - It is without MLRun Source/Target, but you can use your own python code