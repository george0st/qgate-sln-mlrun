# Redis as on-line feature store

## 1. Preconditions for OS Windows

1. Installed **Docker Desktop with WSL 2**
2. You can test success installation
   - check Docker Desktop, cmd `docker --version`
   - check WSL2, cmd `wsl --status` (expected info 'Default Version: 2')
   - check installed distributions, cmd `wsl -l` (expected info 'docker-desktop' and 'docker-desktop-data')

## 2. Run Redis (in container)

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

## 3. Use Redis for tests

 - Update `qgate-sln-mlrun.env`, change setting for `QGATE_REDIS`
   - see `QGATE_REDIS = redis://localhost:6379`
 - Note
   - Port is based on container see **6379**, you can use also different 
   protocol see **rediss**, more informations see [Redis targes store from MLRun](https://docs.mlrun.org/en/latest/data-prep/ingest-data-fs.html#redis-target-store)

