[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version fury.io](https://badge.fury.io/py/qgate-sln-mlrun.svg)](https://pypi.python.org/pypi/qgate-sln-mlrun/)
![coverage](https://github.com/george0st/qgate-sln-mlrun/blob/master/coverage.svg?raw=true)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/george0st/qgate-sln-mlrun)
![GitHub release](https://img.shields.io/github/v/release/george0st/qgate-sln-mlrun)

# QGate-Sln-MLRun
The Quality Gate for solution MLRun (and Iguazio). The main aims of the project are:
- independent quality test (function, integration, acceptance, ... tests)
- deeper quality checks before full rollout/use in company environments
- identification of possible compatibility issues (if any)
- external and independent test coverage
- etc.

The tests use these key components, MLRun solution see **[GIT mlrun](https://github.com/mlrun/mlrun)**, 
sample meta-data model see **[GIT qgate-model](https://github.com/george0st/qgate-model)** and this project.

## Test scenarios
The quality gate covers these test scenarios (✅ done, ❌ in-progress/planned):
 - **Project**
   - ✅ TS101: Create project(s)
   - ✅ TS102: Delete project(s)
 - **Feature set**
   - ✅ TS201: Create feature set(s)
 - **Ingest data**
   - ✅ TS301: Ingest data to feature set(s)
 - **Feature vector**
   - ✅ TS401: Create feature vector(s)
 - **Get data**
   - ✅ TS501: Get data from off-line feature vector(s)
   - ✅ TS502: Get data from on-line feature vector(s)
 - **Build model**
   - ✅ TS601: Build CART model
   - ❌ TS602: Build XGBoost model
   - ❌ TS603: Build DNN model
 - **Serve score**
   - ❌ TS701: Serving score from CART
   - ❌ TS702: Serving score from XGBoost
   - ❌ TS703: Serving score from DNN
   
NOTE: Each test scenario contains addition specific test cases.
    
## Sample of outputs

![Sample of outputs](https://github.com/george0st/qgate-sln-mlrun/blob/master/assets/imgs/qgt-mlrun-samples.png?raw=true)

The reports in original form, see:
 - all DONE - [HTML](https://htmlpreview.github.io/?https://github.com/george0st/qgate-sln-mlrun/blob/master/docs/samples/outputs/qgt-mlrun-sample.html), 
   [TXT](https://github.com/george0st/qgate-sln-mlrun/blob/master/docs/samples/outputs/qgt-mlrun-sample.txt?raw=true)
 - with ERR - [HTML](https://htmlpreview.github.io/?https://github.com/george0st/qgate-sln-mlrun/blob/master/docs/samples/outputs/qgt-mlrun-sample-err.html),
   [TXT](https://github.com/george0st/qgate-sln-mlrun/blob/master/docs/samples/outputs/qgt-mlrun-sample-err.txt?raw=true)

## Usage

You can easy use this solution in four steps:
1. Download content of these two GIT repositories to your local environment
    - [qgate-sln-mlrun](https://github.com/george0st/qgate-sln-mlrun)
    - [qgate-model](https://github.com/george0st/qgate-model)
2. Update file `qgate-sln-mlrun.env` from qgate-model
   - Update variables for MLRun/Iguazio, see `MLRUN_DBPATH`, `V3IO_USERNAME`, `V3IO_ACCESS_KEY`, `V3IO_API`
     - setting of `V3IO_*` is needed only in case of Iguazio installation (not for pure free MLRun)
   - Update variables for QGate, see `QGATE_*` (basic description directly in *.env)
     - detail setup [configuration](./docs/configuration.md)
3. Run from `qgate-sln-mlrun`
   - **python main.py**
4. See outputs
   - './output/qgt-mlrun-*.html'
   - './output/qgt-mlrun-*.txt'

Precondition: You have available MLRun or Iguazio solution (MLRun is part of that),
see official [installation steps](https://docs.mlrun.org/en/latest/install.html), or directly installation for [Desktop Docker](https://docs.mlrun.org/en/latest/install/local-docker.html). 

## Tested with
The project was tested with these MLRun versions (see [change log](https://docs.mlrun.org/en/latest/change-log/index.html)):
 - **MLRun** (in Desktop Docker)
   - MLRun 1.5.2, 1.5.1, 1.5.0
   - MLRun 1.4.1
   - MLRun 1.3.0
 - **Iguazio** (k8s, on-prem with VM with VMware)
   - Iguazio 3.5.3 (with MLRun 1.4.1)
   - Iguazio 3.5.1 (with MLRun 1.3.0)

NOTE: Current state, only the last MLRun/Iguazio versions are valid for testing.

## TODO list
The list of expected/future improvements [see](./docs/todo_list.md) 