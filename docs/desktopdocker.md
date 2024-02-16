# Desktop Docker


1. Installed **Docker Desktop with WSL 2**
2. You can test success installation
   - check Docker Desktop, cmd `docker --version`
   - check WSL2, cmd `wsl --status` (expected info 'Default Version: 2')
   - check installed distributions, cmd `wsl -l` (expected info 'docker-desktop' and 'docker-desktop-data')

Note:
  - In case of issues, it is useful to use by default distribution 'docker-desktop'
    - you can use this command for correct setup `wsl -s docker-desktop`
  - In case of isses, you can use different distribution e.g. 'ubuntu'
    - see command `wsl --install -d Ubuntu`
