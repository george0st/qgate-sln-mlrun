import mlrun.feature_store.steps as fsteps
from qgate_sln_mlrun.helper.generateid import GenerateId


class PipelineHelper():

    def __init__(self, featureset, setting):
        self._featureset = featureset
        self._setting = setting

    def add(self):
        # add pipelines
        if self._setting:
            last_step=None

            # add steps
            if self._setting.get("Imputer"):
                last_step=self._featureset.graph.add_step(fsteps.Imputer(mapping=self._setting['Imputer']),
                                                          name="Imputer",
                                                          after=None if not last_step else last_step.name)

            if self._setting.get("OneHotEncoder"):
                last_step = self._featureset.graph.add_step(fsteps.OneHotEncoder(mapping=self._setting['OneHotEncoder']),
                                                            name="OneHotEncoder",
                                                            after=None if not last_step else last_step.name)

            if self._setting.get("DateExtractor"):
                last_step = self._featureset.graph.add_step(fsteps.DateExtractor(parts=self._setting['DateExtractor']['parts'],
                                                                                 timestamp_col=self._setting['DateExtractor']['timestamp_col']),
                                                            name="DateExtractor",
                                                            after=None if not last_step else last_step.name)

            if self._setting.get("MapValues"):
                # TODO: remove workaround see https://github.com/mlrun/mlrun/issues/5743 (after repair, issue in MLRun 1.6.3)
                last_step = self._featureset.graph.add_step(fsteps.MapValues(mapping=self._setting['MapValues'],
                                                                             with_original_features=True),
                                                            name="MapValues",
                                                            after=None if not last_step else last_step.name)

            if self._setting.get("DropFeatures"):
                last_step = self._featureset.graph.add_step(fsteps.DropFeatures(features=self._setting['DropFeatures']),
                                                            name="DropFeatures",
                                                            after=None if not last_step else last_step.name)

            # own step
            if self._setting.get("GenerateId"):
                last_step = self._featureset.graph.add_step(GenerateId(namespace=self._setting['GenerateId']["namespace"],
                                                                                  features=self._setting['GenerateId']["features"]),
                                                            name="GenerateId",
                                                            after=None if not last_step else last_step.name)

            # storey steps (works only in engine 'storey', it is valid for engine 'spark' or 'pandas')
            if self._setting.get("storey.Filter"):
                last_step=self._featureset.graph.add_step("storey.Filter",
                                                          name="storey.Filter",
                                                          after=None if not last_step else last_step.name,
                                                          _fn=f"{self._setting['storey.Filter']}")

            if self._setting.get("storey.Extend"):
                last_step=self._featureset.graph.add_step("storey.Extend",
                                                          name="storey.Extend",
                                                          after=None if not last_step else last_step.name,
                                                          _fn=f"{self._setting['storey.Extend']}")

        # https://docs.mlrun.org/en/latest/feature-store/transformations.html
        #ok - Imputer
        #ok - OneHotEncoder
        #ok - DateExtractor
        #ok - MapValues
        #ok - DropFeatures

        #MLRunStep


