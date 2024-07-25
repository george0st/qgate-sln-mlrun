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

3. Test Redis in container
   - interactive access to the container
     - `docker exec -it mlrun-redis redis-cli`
   - set key 'aa' to the value '100'
     - `set aa 100`
   - set key 'aa' to the value '100' with expiration 10 seconds
     - `set key 100 ex 10`
   - get key 'aa'
     - `get aa`
   - check if the key 'aa' exist
     - `exists aa`
   - delete key 'aa'
     - `del aa`


## 3. Use Redis for tests

 - Update `qgate-sln-mlrun.env`, change setting for `QGATE_REDIS`
   - pattern see `<redis|rediss>://<host>[:port]`
   - real usage, see `QGATE_REDIS = redis://localhost:6379`
 - Note
   - Port is based on container see **6379**, you can use also different 
   protocol see **rediss**, more information see [Redis targes store from MLRun](https://docs.mlrun.org/en/latest/feature-store/sources-targets.html#redis-target)