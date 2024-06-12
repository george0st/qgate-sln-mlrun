

class TSPipeline():

    def __init__(self, featureset, setting):
        self.featureset = featureset
        self.setting = setting

    def add_pipeline(self):
        # get existing feature set (feature set have to be created in previous test scenario)
        # add pipelines

        if self.setting:
            last_step=None
            # add steps
            if self.setting.get("Imputer"):
                last_step=self.featureset.graph.add_step(fsteps.Imputer(mapping=self.setting['Imputer']),
                                         name="Imputer",
                                         after=None if not last_step else last_step.name)

            if self.setting.get("OneHotEncoder"):
                last_step = self.featureset.graph.add_step(fsteps.OneHotEncoder(mapping=self.setting['OneHotEncoder']),
                                                      name="OneHotEncoder",
                                                      after=None if not last_step else last_step.name)

            if self.setting.get("DateExtractor"):
                last_step = self.featureset.graph.add_step(fsteps.DateExtractor(parts=self.setting['DateExtractor']['parts'],
                                                                           timestamp_col=self.setting['DateExtractor']['timestamp_col']),
                                                      name="DateExtractor",
                                                      after=None if not last_step else last_step.name)

            if self.setting.get("MapValues"):
                # TODO: remove workaround see https://github.com/mlrun/mlrun/issues/5743 (after repair, issue in MLRun 1.6.3)
                last_step = self.featureset.graph.add_step(fsteps.MapValues(mapping=self.setting['MapValues'],
                                                                       with_original_features=True),
                                                      name="MapValues",
                                                      after=None if not last_step else last_step.name)

            if self.setting.get("DropFeatures"):
                last_step = self.featureset.graph.add_step(fsteps.DropFeatures(features=self.setting['DropFeatures']),
                                                      name="DropFeatures",
                                                      after=None if not last_step else last_step.name)

            # own step
            if self.setting.get("GenerateId"):
                last_step = self.featureset.graph.add_step(generateid.GenerateId(namespace=self.setting['GenerateId']["namespace"],
                                                                            features=self.setting['GenerateId']["features"]),
                                                      name="GenerateId",
                                                      after=None if not last_step else last_step.name)

            # storey steps (works only in engine 'storey', it is valid for engine 'spark' or 'pandas')
            if self.setting.get("storey.Filter"):
                last_step=self.featureset.graph.add_step("storey.Filter",
                                     name="storey.Filter",
                                     after=None if not last_step else last_step.name,
                                     _fn=f"{self.setting['storey.Filter']}")

            if self.setting.get("storey.Extend"):
                last_step=self.featureset.graph.add_step("storey.Extend",
                                         name="storey.Extend",
                                         after=None if not last_step else last_step.name,
                                         _fn=f"{self.setting['storey.Extend']}")

        # https://docs.mlrun.org/en/latest/feature-store/transformations.html
        #ok - Imputer
        #ok - OneHotEncoder
        #ok - DateExtractor
        #ok - MapValues
        #ok - DropFeatures

        #MLRunStep

        self.featureset.save()

