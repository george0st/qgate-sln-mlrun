"""
  TS601: Simple pipeline for DataFrame source
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun.feature_store as fstore
import mlrun
import pandas as pd
import glob
import os


class TS601(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Simple pipeline for DataFrame source"

    @property
    def long_desc(self):
        return "Simple pipeline for DataFrame source"

    def exec(self, project_name):
        """Simple pipeline during ingest"""
        return

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

    @TSBase.handler_testcase
    def _ingest_data(self, testcase_name, project_name, featureset_name, file):
        # get existing feature set (feature set have to be created in previous test scenario)
        featureset = fstore.get_feature_set(f"{project_name}/{featureset_name}")

        #quotes_set.graph.to("storey.Filter", "filter", _fn="(event['bid'] > 50)")
        #https://docs.mlrun.org/en/latest/serving/getting-started.html



        # ingest data with bundl/chunk
        for data_frm in pd.read_csv(file,
                                    sep=self.setup.csv_separator,       #";",
                                    header="infer",
                                    decimal=self.setup.csv_decimal,     #",",
                                    compression="gzip",
                                    encoding="utf-8",
                                    chunksize=10000):
            featureset.ingest(data_frm,
                          # overwrite=False,
                          return_df=False,
                          #infer_options=mlrun.data_types.data_types.InferOptions.Null)
                          infer_options=mlrun.data_types.data_types.InferOptions.default())
            # TODO: use InferOptions.Null with python 3.10 or focus on WSL
            # NOTE: option default, change types
            # NOTE: option Null, generate error with datetime in python 3.9
