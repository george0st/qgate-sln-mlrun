import mlrun.feature_store.steps as fsteps
from qgate_sln_mlrun.helper.generateid import GenerateId
from qgate_sln_mlrun.ts.tsbase import TSBase
from qgate_sln_mlrun.setup import Setup
import os
import glob
import json


class PipelineHelper():

    def __init__(self, featureset_name):
        self._setting = self._get_setting(featureset_name)

    @property
    def exist(self):
        return True if self._setting else False

    def add(self, featureset):
        # add pipelines
        if self._setting:
            last_step=None

            # add steps, see https://docs.mlrun.org/en/latest/feature-store/transformations.html

            # remove None, Nan, ... values
            if self._setting.get("Imputer"):
                last_step=featureset.graph.add_step(fsteps.Imputer(mapping=self._setting['Imputer']),
                                                          name="Imputer",
                                                          after=None if not last_step else last_step.name)

            # decode to numeric value
            if self._setting.get("OneHotEncoder"):
                last_step = featureset.graph.add_step(fsteps.OneHotEncoder(mapping=self._setting['OneHotEncoder']),
                                                            name="OneHotEncoder",
                                                            after=None if not last_step else last_step.name)

            # extract date value from datetime
            if self._setting.get("DateExtractor"):
                last_step = featureset.graph.add_step(fsteps.DateExtractor(parts=self._setting['DateExtractor']['parts'],
                                                                                 timestamp_col=self._setting['DateExtractor']['timestamp_col']),
                                                            name="DateExtractor",
                                                            after=None if not last_step else last_step.name)
            # transform values
            if self._setting.get("MapValues"):
                # TODO: must keep 'with_original_features=True', remove workaround see https://github.com/mlrun/mlrun/issues/5743 (after repair, issue in MLRun 1.6.3)
                last_step = featureset.graph.add_step(fsteps.MapValues(mapping=self._setting['MapValues'],
                                                                             with_original_features=True),
                                                            name="MapValues",
                                                            after=None if not last_step else last_step.name)

            # remove feature
            if self._setting.get("DropFeatures"):
                last_step = featureset.graph.add_step(fsteps.DropFeatures(features=self._setting['DropFeatures']),
                                                            name="DropFeatures",
                                                            after=None if not last_step else last_step.name)

            # own step, generate unique Id
            if self._setting.get("GenerateId"):
                last_step = featureset.graph.add_step(GenerateId(namespace=self._setting['GenerateId']["namespace"],
                                                                                  features=self._setting['GenerateId']["features"]),
                                                            name="GenerateId",
                                                            after=None if not last_step else last_step.name)

            # storey steps (works only in engine 'storey', it is valid for engine 'spark' or 'pandas')
            if self._setting.get("storey.Filter"):
                last_step=featureset.graph.add_step("storey.Filter",
                                                          name="storey.Filter",
                                                          after=None if not last_step else last_step.name,
                                                          _fn=f"{self._setting['storey.Filter']}")

            if self._setting.get("storey.Extend"):
                last_step=featureset.graph.add_step("storey.Extend",
                                                          name="storey.Extend",
                                                          after=None if not last_step else last_step.name,
                                                          _fn=f"{self._setting['storey.Extend']}")

    def _get_setting(self, featureset_name):
        source_file = os.path.join(os.getcwd(),
                                   Setup().model_definition,
                                   "01-model",
                                   "04-pipeline",
                                   f"*-{featureset_name}.json")

        # get pipeline definition
        for file in glob.glob(source_file):
            with open(file, "r") as json_file:
                json_content = json.load(json_file)
            name, desc, lbls, kind = TSBase.get_json_header(json_content)

            if kind == "pipeline":
                return json_content['spec']
        return None
