# QGate-Sln-MLRun
Quality Gate for solution MLRun (and Iguazio). The main aims of the project are:
- independent quality test (function, integration, acceptance, ... tests)
- deeper quality checks before full rollout/use in company environments
- identification of compatibility issues (if any)
- external and independent test coverage
- etc.

The tests use these key components:
 - MLRun solution (used in Iguazio solution also), see **[GIT mlrun](https://github.com/mlrun/mlrun)**
 - Sample meta-data model, see **[GIT qgate-model](https://github.com/george0st/qgate-model)**
 - This project

## Usage
You can easy use this solution in three steps:
1. Download content of these two GIT repositories to your local environment
    - [qgate-sln-mlrun](https://github.com/george0st/qgate-sln-mlrun)
    - [qgate-model](https://github.com/george0st/qgate-model)
2. Update file `qgate-sln-mlrun.env` from qgate-model
   - Update variables for MLRun/Iguazio, see `MLRUN_DBPATH`, `V3IO_USERNAME`, `V3IO_ACCESS_KEY`, `V3IO_API`
     - setting of `V3IO_*` is needed only in case of Iguazio installation (not for pure free MLRun)
   - Update variables for QGate, see `QGATE_*`
3. Run from `qgate-sln-mlrun`
   - **python main.py**

Precondition: You have available MLRun or Iguazio solution (MLRun is part of that), see official [installation steps](https://docs.mlrun.org/en/latest/install.html)

## Use cases
Quality Gate covers these use cases:
 - **Project**
   - [x] UC101: Create project
   - [ ] UC102: Delete project
 - **Feature set**
   - [ ] UC201: Create feature sets (with entities, features, targets) 
   - [ ] UC202: Create feature vector
 - **Ingest data**
   - [ ] UC301: Ingest data to feature sets
 - **Feature vector**
   - [ ] UC401: Get data from one feature set
   - [ ] UC402: Join data from two feature sets
   - [ ] UC403: Join data from four feature sets

## Tested with
The project was test with these versions (see [change log](https://docs.mlrun.org/en/latest/change-log/index.html)):
 - Iguazio (k8s, on-prem with VM with VMware)
   - Iguazio 3.5.3 (with MLRun 1.4.1)
   - Iguazio 3.5.1 (with MLRun 1.3.0)
 - MLRun (in Desktop Docker)
   - MLRun 1.5.1, 1.5.0
   - MLRun 1.4.1
   - MLRun 1.3.0
