# Spark as engine

## 1. Preconditions for OS Windows

 - Install Desktop Docker, [see](./desktopdocker.md)

## 2. Run Spark (in container)

1. Get image from official source
   - get specific Spark image version 8.3 `docker pull spark:3.5.1-python3`
   - or get last Spark image `docker pull spark:latest`
   - Note
     - available [versions](https://hub.docker.com/_/spark)/[tags](https://hub.docker.com/_/spark/tags)

2. Run new container
   - create container with name 'mlrun-spark', use image 'spark:3.5.1-python3' and open ports ???:???
     - `docker run --name mlrun-spark -d spark:3.5.1-python3`
   - or create container with name 'mlrun-spark', use image 'spark:latest' and open ports ???:???
     - `docker run --name mlrun-spark -d spark:latest`
   - NOTE:
     - user `??`, password `??`

3. Test Spark in container
   - interactive access to the container
     - `docker exec -it mlrun-spark bash`

## 3. Use Spark for tests

 - Update `qgate-sln-mlrun.env`, change setting for `QGATE_SPARK`
   - format `QGATE_SPARK = `
   - see `QGATE_SPARK = `
