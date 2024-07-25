# Cassandra as on-line source/target

## 1. Preconditions for OS Windows

 - Install Desktop Docker, [see](./desktopdocker.md)

## 2. Run Cassandra (in container)

1. Get image from official source
   - get specific redis image version 7.2 `docker pull redis:7.2`
   - or get last redis image `docker pull redis:latest`
   - Note
     - available [versions](https://hub.docker.com/_/redis)/[tags](https://hub.docker.com/_/redis/tags)

2. Run new container
   - create container with name 'mlrun-redis', use image 'redis:7.2' and open ports 6379:6379
     - `docker run --name mlrun-redis -p 6379:6379 -d redis:7.2`
   - or create container with name 'mlrun-redis', use image 'redis:latest' and open ports 6379:6379
     - `docker run --name mlrun-redis -p 6379:6379 -d redis:latest`

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
