# QGate-MLRun
Quality Gate for solution MLRun and Iguazio. The main aims of the project are:
- independent quality test (function, integration, acceptance, performance, ... tests) of MLRun/Iguazio versions
- identification of compatibility issues
- deeper quality checks
- automatization
- etc.

The tests use these key components:
 - MLRun solution (used in Iguazio solution also), see **[GIT MLRun](https://github.com/mlrun/mlrun)**
 - sample data model, see **[GIT QGate-FS-Model](https://github.com/george0st/qgate-fs-model)**
 - etc.

## Usage
You can easy use this solution in three steps:
1. Download content of these two GIT repository to your local environment
    - [QGate-MLRun](https://github.com/george0st/qgate-mlrun)
    - [QGate-FS-Model](https://github.com/george0st/qgate-fs-model)
2. Update file `qgate-mlrun.env` from QGate-FS-Model
   - Update variables for MLRun/Iguazio, see `MLRUN_DBPATH`, `V3IO_USERNAME`, `V3IO_ACCESS_KEY`, `V3IO_API`
   - Update variables for QGate, see `QGATE-FS-MODEL`
3. Run from QGate-MLRun
   - **python main.py**

Precondition: You have available MLRun or Iguazio solution, see [installation steps](https://docs.mlrun.org/en/latest/install.html)