# Pyenv usage

### 1. Setting pyenv
pyenv install 3.9
pyenv global 3.9

### 2. Clone GIT repo `qgate-sln-mlrun`
git clone git@github.com:george0st/qgate-sln-mlrun.git
cd qgate-sln-mlrun

### 3. Create virtual environment
python -m venv venv
source venv/bin/activate

### 4. Upgrade PIP
pip install --upgrade pip

### 5. Install requirements
pip install -r requirements.txt
