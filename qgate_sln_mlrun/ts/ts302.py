"""
  TS302: Ingest data to feature set(s) from CSV Source
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore
from mlrun.data_types.data_types import spark_to_value_type
from mlrun.datastore.sources import CSVSource
import pandas as pd
import glob
import os


class TS302(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Ingest data to feature set(s) from CSV source "

    @property
    def long_desc(self):
        return "Ingest data to feature set(s) from CSV source"

    def exec(self, project_name):
        """Data ingest"""
        for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
            # create possible file for load
            source_file = os.path.join(os.getcwd(),
                                       self.setup.model_definition,
                                       "02-data",
                                       self.setup.dataset_name,
                                       f"*-{featureset_name}.csv.gz")

            # check existing data set
            for file in glob.glob(source_file):
                self._ingest_data(f"{project_name}/{featureset_name}", project_name, featureset_name, file)

    # def ingest_data(self):
    #     """Data ingest
    #     """
    #     self.testscenario_new()
    #     for project_name in self.projects:
    #         for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
    #             # create possible file for load
    #             source_file=os.path.join(os.getcwd(),
    #                                      self.setup.model_definition,
    #                                      "02-data",
    #                                      self.setup.dataset_name,
    #                                      f"*-{featureset_name}.csv.gz")
    #
    #             # check existing data set
    #             for file in glob.glob(source_file):
    #                 self._ingest_data( f"{project_name}/{featureset_name}", project_name, featureset_name, file)

    @TSBase.handler_testcase
    def _ingest_data(self, testcase_name, project_name, featureset_name, file):
        # get existing feature set (feature set have to be created in previous test scenario)
        featureset = fstore.get_feature_set(f"{project_name}/{featureset_name}")

        fstore.ingest(featureset,
                      CSVSource(name="tst", path=file),
                      # overwrite=False,
                      return_df=False,
                      #infer_options=mlrun.data_types.data_types.InferOptions.Null)
                      infer_options=mlrun.data_types.data_types.InferOptions.default())
        # TODO: use InferOptions.Null with python 3.10 or focus on WSL
        # NOTE: option default, change types
        # NOTE: option Null, generate error with datetime in python 3.9




