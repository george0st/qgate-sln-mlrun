# MLRun/Iguazio, the KEY changes in a nutshell

NOTE: 
 - You can see detail changes in
   - [MLRun change log](https://docs.mlrun.org/en/latest/change-log/index.html)
   - [Iguazio change log](https://www.iguazio.com/docs/latest-release/release-notes/)
   - [Iguazio mng. change log](https://iguazio.github.io/igz-mgmt-sdk/changelog.html)
 - Legend
   - 🚩 future version, ✅ current version 

## MLRun

### 🚩1.7 MLRun
 - Model monitoring/drifting for MLRun (available in free version also)
 - Available API Gateway (better configuration)
 - Improve scaling for Nuclio (from version >= 1.13)
 - Support paging (ability to return long data)
 - NOTE:
   - Expected release date 05/2024 (based on 3 months release cycle)

### ✅ 1.6 MLRun
 - Model monitoring/drifting for Iguazio (V3IO support only)
 - MLFlow integration (store artifact to MLRun)
 - Support Pandas 2.0 (improve performance)
 - Extend datastore profiles (add providers)

### 1.5 MLRun
 - Datastore profiles
 - Improve FeatureVector join

## Iguazio

### ✅ 3.5.5 Iguazio
 - Supports self-signed docker-registries
 - support full SSO with Keycloak (useful for end users)
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
