# Applied limits for MLRun Quality Gate

1. The MLRun Client (in version 1.5.2) **does not support OS Windows**, 
see [ML-4907](https://docs.mlrun.org/en/latest/change-log/index.html#limitations)
   - know issues with datatime conversion in python 3.9 (under OS Windows)
   - missing MLRun tests under OS Windows
   - others (without addition details)
   
2. The data read (via feature vector) **accept only one on-line and
   one off-line target** in FeatureSet, see [Slack discussion](https://mlopslive.slack.com/archives/C014XCMNY4Q/p1701025414893399?thread_ts=1701021926.280329&cid=C014XCMNY4Q)
   - in case of e.g. more on-line targets, it is not possible to choose 
   relevant for FeatureVector  