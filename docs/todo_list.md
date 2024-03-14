# TODO list

The list of expected/future improvements:
 
 1. **Add tests with MySQL...**
    - It is important to solve schema mapping issue in MySQL source
    - Why?
      - Add bigger variability for usage

 2. **Solve issue with project delete**
    - see mistake in MLRun 1.6.1
    
 3. **Extend QGATE_OUTPUT as arraylist**
    - support more storages S3, BlobStorage
    
 3. **Test target in S3**
    - add secrets for S3 login

 4. **Test target in BlobStorage**
    - add secrets for BlobStorage

 5. TBD.
 
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