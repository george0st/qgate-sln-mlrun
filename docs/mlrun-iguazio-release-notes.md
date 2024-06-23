# MLRun/Iguazio, the KEY changes in a nutshell

You can see detail changes in 
   - [MLRun change log](https://docs.mlrun.org/en/latest/change-log/index.html)
   - [Iguazio change log](https://www.iguazio.com/docs/latest-release/release-notes/)
   - [Iguazio mng. change log](https://iguazio.github.io/igz-mgmt-sdk/changelog.html)
   - Legend
     - 🚩 future version, ✅ current version 

## MLRun

### 🚩1.8 MLRun (exp. 11/2024)
 - Focus on SourceSQL, TargetSQL
 - TBD.

### 🚩1.7 MLRun (exp. 07/2024)
 - Model monitoring/drifting for MLRun (available in free version also)
 - Available API Gateway (flexible configuration & Nuclio tuning)
 - Improve scaling for Nuclio (from version >= 1.13)
 - Support paging (ability to return longer data)
 - Support HDFS as data store (via WebHDFS)
 - Support Spark Streaming

### ✅ 1.6 MLRun
 - Model monitoring/drifting for Iguazio (V3IO support only)
 - MLFlow integration (store artifact to MLRun, [see](https://docs.mlrun.org/en/latest/tutorials/mlflow.html))
 - Support Pandas 2.0 (improve performance)
 - Extend datastore profiles (addition providers)

### 1.5 MLRun
 - Datastore profiles
 - Improve FeatureVector join

## Iguazio

### ✅ 3.6.0 Iguazio
 - Supports Rocky Linux 8.x OS & Kubernetes 1.28 for on-prem vanilla 
 - Focused on fixes
   - All ingresses using secured traffic (SSL), periodic deletion of files on var/crash on app nodes, etc.
 - Important note:
   - Announcement future deprecation, 'V3IO NoSQL (key-value) and streams functionality will be deprecated in the next major release.' 

### 3.5.5 Iguazio
 - Supports self-signed docker-registries
 - Support full SSO with Keycloak (useful for end users)
 - K8s 1.28

### 3.5.4 Iguazio
 - Addition new role 'IT Admin Read Only'
 - Support the i3.2xlarge AWS
 - Deprecated python 3.6 and 3.7
 - K8s 1.26

### 3.5.4 Iguazio
 - JupyterLab 3.4.8
 - Support python 3.9
 - K8s 1.24
