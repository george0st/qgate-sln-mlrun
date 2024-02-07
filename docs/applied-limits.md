# Applied limits for MLRun Quality Gate

1. The MLRun Client (in version 1.5.2) **does not support OS Windows**, 
see [ML-4907](https://docs.mlrun.org/en/latest/change-log/index.html#limitations). Know issues:
   - mistake in datatime conversion under python 3.9 and OS Windows, see [issue](https://stackoverflow.com/questions/77743056/python-oserror-errno-22-invalid-argument-for-datetime-timestamp)
   - it is necessary to use Linux path (not Windows path) for some cases e.g. for [CSVTarget](https://github.com/mlrun/mlrun/issues/5056)
   - missing MLRun tests under OS Windows
   - probably others (without full tracking and addition details)
   
2. The data read (via feature vector) **accept only one on-line and
   one off-line target** in FeatureSet, see [Slack discussion](https://mlopslive.slack.com/archives/C014XCMNY4Q/p1701025414893399?thread_ts=1701021926.280329&cid=C014XCMNY4Q)
   - in case of e.g. more on-line targets, it is not possible to choose 
   relevant for FeatureVector  