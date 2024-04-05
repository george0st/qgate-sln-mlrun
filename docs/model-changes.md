# Changes in QGate model

If you need to change the file in QGate model for specific
solution e.g. for the Iguazio/MLRun, follow these steps:

 1. copy the file from '../qgate_model', to the folder
    './qgate_sln_<solution>/model_changes'
 2. update the file

## What will the system do?
In case of load file from '../qgate_model':
 
1. the system will check, if the same file name is in the folder 
  './gate_sln_<solution>/model_changes'
2. if yes, the system will use the file from
  './qgate_sln_<solution>/model_changes'

## Limits

It covers content replacement for these paths:
  - **'./qgate-model/01-model/01-project/*'**
  - other paths, can be later added

