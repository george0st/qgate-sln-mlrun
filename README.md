[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI version fury.io](https://badge.fury.io/py/qgate-sln-mlrun.svg)](https://pypi.python.org/pypi/qgate-sln-mlrun/)
![coverage](https://github.com/george0st/qgate-sln-mlrun/blob/master/coverage.svg?raw=true)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/george0st/qgate-sln-mlrun)
![GitHub release](https://img.shields.io/github/v/release/george0st/qgate-sln-mlrun)

# QGate-Sln-MLRun
The Quality Gate for solution [MLRun](https://www.mlrun.org/) (and [Iguazio](https://www.iguazio.com/)). The main aims of the project are:
- independent quality test (function, integration, acceptance, ... tests)
- deeper quality checks before full rollout/use in company environments
- identification of possible compatibility issues (if any)
- external and independent test coverage
- etc.

The tests use these key components, MLRun solution see **[GIT mlrun](https://github.com/mlrun/mlrun)**, 
sample meta-data model see **[GIT qgate-model](https://github.com/george0st/qgate-model)** and this project.

## Test scenarios
The quality gate covers these test scenarios (✅ done, ✔ in-progress, ❌ planned):
 - **01 - Project**
   - ✅ TS101: Create project(s)
   - ✅ TS102: Delete project(s)
 - **02 - Feature set**
   - ✅ TS201: Create feature set(s)
   - ✅ TS202: Create feature set(s) & Ingest from DataFrame source (one step)
   - ✅ TS203: Create feature set(s) & Ingest from CSV source (one step) 
   - ✅ TS204: Create feature set(s) & Ingest from Parquet source (one step)
   - ✅ TS205: Create feature set(s) & Ingest from SQL source (one step)
   - ✔  TS206: Create feature set(s) & Ingest from Kafka source (one step)
   - ❌ TS207: Create feature set(s) & Ingest from HTTP source (one step)
 - **03 - Ingest data**
   - ✅ TS301: Ingest data (Preview mode)
   - ✅ TS302: Ingest data to feature set(s) from DataFrame source
   - ✅ TS303: Ingest data to feature set(s) from CSV source 
   - ✅ TS304: Ingest data to feature set(s) from Parquet source
   - ✅ TS305: Ingest data to feature set(s) from SQL source
   - ✔  TS306: Ingest data to feature set(s) from Kafka source
   - ❌ TS307: Ingest data to feature set(s) from HTTP source
 - **04 - Ingest data & pipeline**
   - ❌ TS401: Ingest data & pipeline (Preview mode)
   - ❌ TS402: Ingest data & pipeline to feature set(s) from DataFrame source
   - ❌ TS403: Ingest data & pipeline to feature set(s) from CSV source 
   - ❌ TS404: Ingest data & pipeline to feature set(s) from Parquet source
   - ❌ TS405: Ingest data & pipeline to feature set(s) from SQL source
   - ❌ TS406: Ingest data & pipeline to feature set(s) from Kafka source
   - ❌ TS407: Ingest data & pipeline to feature set(s) from HTTP source
 - **04 - Feature vector**
   - ✅ TS401: Create feature vector(s)
 - **05 - Get data from vector**
   - ✅ TS501: Get data from off-line feature vector(s)
   - ✅ TS502: Get data from on-line feature vector(s)
 - **06 - Pipeline**
   - ✅ TS601: Simple pipeline(s)
   - ✅ TS602: Complex pipeline(s)
   - ✅ TS603: Complex pipeline(s), mass operation
   - ✔  TS604: Complex pipeline(s) for ingest
 - **07 - Build model**
   - ✅ TS701: Build CART model
   - ❌ TS702: Build XGBoost model
   - ❌ TS703: Build DNN model
 - **08 - Serve model**
   - ✅ TS801: Serving score from CART
   - ❌ TS802: Serving score from XGBoost
   - ❌ TS803: Serving score from DNN
 - **09 - Model monitoring/drifting**
   - ❌ TS901: Real-time monitoring
   - ❌ TS902: Batch monitoring
   
NOTE: Each test scenario contains addition specific test cases (e.g. with different
targets for feature sets, etc.).

## Test inputs/outputs
The quality gate tests these inputs/outputs (✅ done, ✔ in-progress, ❌ planned):
 - Outputs (targets)
   - ✅ RedisTarget, ✅ SQLTarget/MySQL, ✔ SQLTarget/Postgres, ✅ KafkaTarget
   - ✅ ParquetTarget, ✅ CSVTarget
   - ✅ File system, ❌ S3, ❌ BlobStorage
 - Inputs (sources)
   - ✅ Pandas/DataFrame, ✅ SQLSource/MySQL, ❌ SQLSource/Postgres, ❌ KafkaSource
   - ✅ ParquetSource, ✅ CSVSource
   - ✅ File system, ❌ S3, ❌ BlobStorage


The current supported [sources/targets in MLRun](https://docs.mlrun.org/en/latest/feature-store/sources-targets.html).

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
4. See outputs (location is based on `QGATE_OUTPUT` in configuration)
   - './output/qgt-mlrun-<date> <timestamp>.html'
   - './output/qgt-mlrun-<date> <timestamp>.txt'

Precondition: You have available MLRun or Iguazio solution (MLRun is part of that),
see official [installation steps](https://docs.mlrun.org/en/latest/install.html), or directly installation for [Desktop Docker](https://docs.mlrun.org/en/latest/install/local-docker.html). 

## Tested with
The project was tested with these MLRun versions (see [change log](https://docs.mlrun.org/en/latest/change-log/index.html)):
 - **MLRun** (in Desktop Docker)
   - MLRun 1.7.0 (plan 05-06/2024)
   - MLRun 1.6.3 (plan 05/2024), 1.6.2, 1.6.1, 1.6.0
   - MLRun 1.5.2, 1.5.1, 1.5.0
   - MLRun 1.4.1, 1.3.0
 - **Iguazio** (k8s, on-prem, VM on VMware)
   - Iguazio 3.5.3 (with MLRun 1.4.1)
   - Iguazio 3.5.1 (with MLRun 1.3.0)

NOTE: Current state, only the last MLRun/Iguazio versions are valid for testing 
(these tests are without back-compatibilities).

## Others
 - **To-Do**, the list of expected/future improvements, [see](./docs/todo_list.md)
 - **Applied limits**, the list of applied limits, [see](./docs/applied-limits.md) 
 - **How can you test the solution?**, you have to focus on Linux env. or 
 Windows with WSL2 ([see](./docs/testing.md) step by step tutorial)
 - **MLRun/Iguazio, the key changes in a nutshell**, [see](./docs/mlrun-iguazio-release-notes.md)
