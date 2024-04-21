# How can you do the testing

### 1. Desktop Docker Setting
You have to setup desktop docker, [see](./desktopdocker.md)

### 2. Pyenv installation
You have to install Pyenv, [see](./pyenv-install.md)

### 3. Pyenv usage
You have to use Pyenv, [see](./pyenv-use.md)

### 4. Use IDE e.g. VSCode
 - run IDE VSCode
 - choose WSL and relevant distribution `WSL: Ubuntu` or `WSL: Ubuntu-20.04` 
 - choose interpreter `python 3.9.x ('venv': venv)'`
 - it is possible to Run/Debug your code

### 5. Tune Docker Desktop
 - Define limit for WSL2
   - define the file `c:\Users\<user>\.wslconfig`
   - define your memory limit (8GB is minimum) for testing 
     - see `[wsl2] memory=8GB`
   - restart WSL2 
 - NOTE: [Full description](https://www.aleksandrhovhannisyan.com/blog/limiting-memory-usage-in-wsl-2/)