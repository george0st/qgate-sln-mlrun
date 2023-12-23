"""
  TS301: Ingest data to feature set(s)
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore
from mlrun.data_types.data_types import spark_to_value_type
import pandas as pd
import json
import glob
import os


class TS301(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Ingest data to feature set(s)"

    @property
    def long_desc(self):
        return "Ingest data to feature set from data source to targets based on feature set definition"

    def exec(self):
        self.ingest_data()

    def ingest_data(self):
        """Data ingest

        :param ts:  Test scenario
        """
        self.testscenario_new()
        for project_name in self.projects:
            for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
                # create possible file for load
                source_file=os.path.join(os.getcwd(),
                                         self.setup.model_definition,
                                         "02-data",
                                         self.setup.data_size,
                                         f"*-{featureset_name}.csv.gz")

                # check existing data set
                for file in glob.glob(source_file):
                    self._ingest_data( f"{project_name}/{featureset_name}", project_name, featureset_name, file)

    @TSBase.handler_testcase
    def _ingest_data(self, testcase_name, project_name, featureset_name, file):
        # get existing feature set (feature set have to be created in previous test scenario)
        featureset = fstore.get_feature_set(f"{project_name}/{featureset_name}")

        # ingest data with bundl/chunk
        for data_frm in pd.read_csv(file,
                                    sep=";",
                                    header="infer",
                                    decimal=",",
                                    compression="gzip",
                                    encoding="utf-8",
                                    chunksize=10000):
            fstore.ingest(featureset,
                          data_frm,
                          # overwrite=False,
                          return_df=False,
                          infer_options=mlrun.data_types.data_types.InferOptions.Null)


