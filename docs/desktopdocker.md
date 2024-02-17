# Desktop Docker

### 1. Installed Docker Desktop with WSL 2

### 2. You can test success installation
   - check Docker Desktop, cmd `docker --version`
   - check WSL2, cmd `wsl --status` (expected info 'Default Version: 2')
   - check installed distributions, cmd `wsl -l` (expected info 'docker-desktop' and 'docker-desktop-data')

**Note:**
  - It is useful to use by default distribution 'docker-desktop'
    - see command `wsl -s docker-desktop`
  - In case of issues, you can use different distribution e.g. 'ubuntu'
    - see command `wsl --install -d Ubuntu`
    - or specific Ubuntu version e.g. `wsl --install -d Ubuntu-20.04`
