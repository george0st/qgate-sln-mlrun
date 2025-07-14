# MLRun/Iguazio, the KEY changes in a nutshell (from my selfish perspective)

You can see detail changes in 
   - [MLRun change log](https://docs.mlrun.org/en/latest/change-log/index.html)
   - [Iguazio change log](https://www.iguazio.com/docs/latest-release/release-notes/)
   - [Iguazio mng. change log](https://iguazio.github.io/igz-mgmt-sdk/changelog.html)
   - Legend
     - 🚩 future version, ✅ published version 

## MLRun

### 🚩 1.10 MLRun (exp. Q4/2025)
 - Postgress support (not only MySQL) 
 - Cleaning (remove obsolete/deprecated code)
 - etc.

### ✅ 1.9 MLRun
 - Support **newer Python version** (>=3.11) and support 3.9

### ✅ 1.8 MLRun
 - Focus on SourceSQL/TargetSQL improvements, [see](https://github.com/mlrun/mlrun/issues/5238#issuecomment-2163887467)
 - GA for Monitoring

### ✅ 1.7 MLRun
 - **Model monitoring/drifting** for MLRun (in free version), relation to MySQL
 - **API Gateway** (flexible configuration & Nuclio tuning, more endpoints, etc.)
 - Support GenAI/LLM (see Langchain, GenAI tutorial, etc.)
 - Improve scaling for Nuclio (from version >= 1.13)
 - Support Hadoop/HDFS (via WebHDFS) and Snowflake as data store
 - Support only Kubernate installation (focus on MLRun CE)

### ✅ 1.6 MLRun
 - Model monitoring/drifting for Iguazio (V3IO support only)
 - MLFlow integration (store artifact to MLRun, [see](https://docs.mlrun.org/en/latest/tutorials/mlflow.html))
 - Support Pandas 2.0 (improve performance)
 - Support paging (ability to return longer data from 1.6.4)
 - Extend datastore profiles (addition providers)

### ✅ 1.5 MLRun
 - Datastore profiles
 - Improve FeatureVector join

## Iguazio

### 🚩 3.7.0 Iguazio (exp. Q4/2025)
 - Remove V3IO NoSQL (key-value), focus on external KV solutions
 - TBD.

### ✅ 3.6.2 Iguazio
 - Support Spark 3.5.3, Spark operator 3.5.2, K8s 1.30.0

### ✅ 3.6.1 Iguazio
 - Supports Kubernetes 1.30 for GKS
 - Bug fixing

### ✅ 3.6.0 Iguazio
 - Supports Rocky Linux 8.x OS & Kubernetes 1.28 for on-prem vanilla 
 - Focused on fixes
   - All ingresses using secured traffic (SSL), periodic deletion of files on var/crash on app nodes, etc.
 - Important announcement:
   - Future deprecation, citation from release notes
     - **'V3IO NoSQL (key-value) and streams functionality will be deprecated in the next major release.'** 

### ✅ 3.5.5 Iguazio
 - Supports self-signed docker-registries
 - Support full SSO with Keycloak (useful for end users)
 - K8s 1.28

### ✅ 3.5.4 Iguazio
 - Addition new role 'IT Admin Read Only'
 - Support the i3.2xlarge AWS
 - Deprecated python 3.6 and 3.7
 - K8s 1.26

### ✅ 3.5.4 Iguazio
 - JupyterLab 3.4.8
 - Support python 3.9
 - K8s 1.24
