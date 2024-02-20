# TODO list

The list of expected/future improvements:

 1. **Split output report based on Projects**
    - Group by Project
    - Why?
      - Increase readeability & Filtering
     
 2. **Test SQLSource and SQLTarget**
    - Focus on MySQL and PostgreSQL in DockerImage
    - Why?
      - Quality gate extension
      - Tests from on/off-line view

 3. **Add tests with Redis/MySQL/...**
    - Why?
      - Add bigger variability for usage

 4. Etc.

## Freeze points

 1. **Test mlrun client under Python 3.10 with OS Windows**
    - Why?
      - Remove issue with datetime under Python 3.9 in OS Windows
      - Ability to use InterferOption.Null and fix redundant data type conversion in TS502
      - Ability to focus on MLRun client usage/development under OS Windows without
      neccessity to use WSL (ability to use PyCharm Community version)
      - other issues, see problems with path to the file system (know issue with CSVTarget)
    - Alternative solution
      - Use VSCode with Linux container under OS Windows