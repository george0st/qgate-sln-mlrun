

class TSPipeline():

    def __init__(self, featureset, setting):
        self.featureset = featureset
        self.setting = setting

    def add_pipeline(self):
        # get existing feature set (feature set have to be created in previous test scenario)
        # add pipelines
        setting=self.test_setting_pipeline['tests'][featureset_name]
        if setting:
            last_step=None
            # add steps
            if setting.get("Imputer"):
                last_step=featureset.graph.add_step(fsteps.Imputer(mapping=setting['Imputer']),
                                         name="Imputer",
                                         after=None if not last_step else last_step.name)

            if setting.get("OneHotEncoder"):
                last_step = featureset.graph.add_step(fsteps.OneHotEncoder(mapping=setting['OneHotEncoder']),
                                                      name="OneHotEncoder",
                                                      after=None if not last_step else last_step.name)

            if setting.get("DateExtractor"):
                last_step = featureset.graph.add_step(fsteps.DateExtractor(parts=setting['DateExtractor']['parts'],
                                                                           timestamp_col=setting['DateExtractor']['timestamp_col']),
                                                      name="DateExtractor",
                                                      after=None if not last_step else last_step.name)

            if setting.get("MapValues"):
                # TODO: remove workaround see https://github.com/mlrun/mlrun/issues/5743 (after repair, issue in MLRun 1.6.3)
                last_step = featureset.graph.add_step(fsteps.MapValues(mapping=setting['MapValues'],
                                                                       with_original_features=True),
                                                      name="MapValues",
                                                      after=None if not last_step else last_step.name)

            if setting.get("DropFeatures"):
                last_step = featureset.graph.add_step(fsteps.DropFeatures(features=setting['DropFeatures']),
                                                      name="DropFeatures",
                                                      after=None if not last_step else last_step.name)

            # own step
            if setting.get("GenerateId"):
                last_step = featureset.graph.add_step(generateid.GenerateId(namespace=setting['GenerateId']["namespace"],
                                                                            features=setting['GenerateId']["features"]),
                                                      name="GenerateId",
                                                      after=None if not last_step else last_step.name)

            # storey steps (works only in engine 'storey', it is valid for engine 'spark' or 'pandas')
            if setting.get("storey.Filter"):
                last_step=featureset.graph.add_step("storey.Filter",
                                     name="storey.Filter",
                                     after=None if not last_step else last_step.name,
                                     _fn=f"{setting['storey.Filter']}")

            if setting.get("storey.Extend"):
                last_step=featureset.graph.add_step("storey.Extend",
                                         name="storey.Extend",
                                         after=None if not last_step else last_step.name,
                                         _fn=f"{setting['storey.Extend']}")

        # https://docs.mlrun.org/en/latest/feature-store/transformations.html
        #ok - Imputer
        #ok - OneHotEncoder
        #ok - DateExtractor
        #ok - MapValues
        #ok - DropFeatures

        #MLRunStep

        featureset.save()

        # ingest data with bundl/chunk
        for data_frm in pd.read_csv(file,
                                    sep=self.setup.csv_separator,
                                    header="infer",
                                    decimal=self.setup.csv_decimal,
                                    compression="gzip",
                                    encoding="utf-8",
                                    chunksize=Setup.MIN_BUNDLE):
            featureset.preview(data_frm)

