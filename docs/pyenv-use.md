# Pyenv usage 

### 1. Install python 3.9 in pyenv 
pyenv install 3.9
pyenv global 3.9

### 2. Clone GIT repo `qgate-sln-mlrun` & `qgate-model`
git clone https://github.com/george0st/qgate-sln-mlrun.git
git clone https://github.com/george0st/qgate-model.git
cd qgate-sln-mlrun

### 3. Create virtual environment
python -m venv venv
source venv/bin/activate

### 4. Upgrade PIP
pip install --upgrade pip

### 5. Install requirements
pip install -r requirements.txt


### NOTE:
 - it is possible to uninstall python version from pyenv via `pyenv uninstall 2.7.15`
 - it is possible to see existing python versions in pyenv via `pyenv versions`