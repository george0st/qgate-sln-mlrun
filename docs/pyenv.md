# Installation pyenv

### 1. Update OS
sudo apt update -y

### 2. Install relevant libraries
sudo apt install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

### 3. Get last pyenv from GitHub
git clone https://github.com/pyenv/pyenv.git ~/.pyenv

### 4. Update bashrc file
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init --path)"' >> ~/.bashrc

### 5. Restart shell
exec "$SHELL"

### 6. Check pyenv version
pyenv --version
