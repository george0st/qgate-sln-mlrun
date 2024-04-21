# How can you do the testing

### 1. Disable 'docker scout' (recommendation)
You can disable the service **docker scout**, it is primary
for vulnerability scanning and reporting and you not need that for testing:
 - see `docker scout repo disable --all`

NOTE: 
 - In case of MLRun function, ... deployment (and create new docker image),
this security scanner can significantly degrade performance based on scanning e.g.
new docker image with size 2 GB.
 - full description, [see](https://docs.docker.com/reference/cli/docker/scout/repo/disable/)

### 2. Tune Docker Desktop (recommendation)
It is useful to define limit for WSL2:
 - define the file `c:\Users\<user>\.wslconfig`
 - define in the file your memory limit (8 GB is minimum) for testing 
   - see `[wsl2] memory=8GB`
 - restart WSL2 

Full description [see](https://www.aleksandrhovhannisyan.com/blog/limiting-memory-usage-in-wsl-2/)

### 3. Desktop Docker Setting
You have to setup desktop docker, [see](./desktopdocker.md)

### 4. Pyenv installation
You have to install Pyenv, [see](./pyenv-install.md)

### 5. Pyenv usage
You have to use Pyenv, [see](./pyenv-use.md)

### 6. Use IDE e.g. VSCode
 - run IDE VSCode
 - choose WSL and relevant distribution `WSL: Ubuntu` or `WSL: Ubuntu-20.04` 
 - choose interpreter `python 3.9.x ('venv': venv)'`
 - it is possible to Run/Debug your code

