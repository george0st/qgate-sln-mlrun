# TODO list

The list of expected/future improvements:
 1. **Test mlrun client under Python 3.10**
    - Why?
      - Remove issue with datetime under Python 3.9 in OS Windows
      - Ability to use InterferOption.Null and fix redundant data type conversion in TS502
      - Ability to focus on MLRun client usage/development under OS Windows without
      neccessity to use WSL (ability to use PyCharm Community version)
 2. **Test SQLSource and SQLTarget**
    - Focus on MySQL and Postgee in DockerImage
    - Why?
      - Check maturity of this solution
      - Tests from on/off-line view 