"""
  TS204: Create feature set(s) & Ingest from Parquet source (one step)
"""
from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore
from mlrun.data_types.data_types import ValueType
from mlrun.datastore.sources import ParquetSource
from qgate_sln_mlrun.ts.ts02_feature_set import ts201
import os
import json
import glob
from qgate_sln_mlrun.helper.featuresethelper import FeatureSetHelper


class TS204(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Create feature set(s) & Ingest from Parquet source (one step)"

    @property
    def long_desc(self):
        return ("Create feature set(s) & Ingest from Parquet source (one step, without save and load featureset)")

    def prj_exec(self, project_name):
        """ Create featuresets and ingest"""

        for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
            # create file with definition of vector
            source_file = os.path.join(os.getcwd(),
                                       self.setup.model_definition,
                                       "01-model",
                                       "02-feature-set",
                                       f"*-{featureset_name}.json")

            for file in glob.glob(source_file):
                # iterate cross all featureset definitions
                with open(file, "r") as json_file:
                    self._create_featureset_ingest(f'{project_name}/{featureset_name}', project_name, json_file)

    @TSBase.handler_testcase
    def _create_featureset_ingest(self, testcase_name, project_name, json_file):
        json_content = json.load(json_file)
        name, desc, lbls, kind = TSBase.get_json_header(json_content)

        if kind == "feature-set":

            # create feature
            fs_helper=FeatureSetHelper(self._solution)
            featureset=fs_helper.create_featureset_content(project_name, f"{self.name}-{name}", desc, json_content['spec'])

            source_file = os.path.join(os.getcwd(),
                                       self.setup.model_definition,
                                       "02-data",
                                       self.setup.dataset_name,
                                       f"*-{name}.parquet")
            for file in glob.glob(source_file):

                fstore.ingest(featureset,
                              ParquetSource(name="tst", path=file),
                              # overwrite=False,
                              return_df=False,
                              # infer_options=mlrun.data_types.data_types.InferOptions.Null)
                              infer_options=mlrun.data_types.data_types.InferOptions.default())
                # TODO: use InferOptions.Null with python 3.10 or focus on WSL
                # NOTE: option default, change types
                # NOTE: option Null, generate error with datetime in python 3.9

