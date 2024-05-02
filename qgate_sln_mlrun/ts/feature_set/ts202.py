"""
  TS202: Create feature set(s) & Ingest from DataFrame source (one step)
"""
from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
from mlrun.data_types.data_types import ValueType
from qgate_sln_mlrun.ts.feature_set import ts201
import os
import json
import glob
import pandas as pd


class TS202(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Create feature set(s) & Ingest from DataFrame source (in one step)"

    @property
    def long_desc(self):
        return ("Create feature set(s) & Ingest from DataFrame source (in one step, without save and load featureset)")

    def exec(self, project_name):
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

            # create feature set based on the logic in TS201
            ts= ts201.TS201(self._solution)
            featureset=ts.create_featureset_content(project_name, f"{self.name}-{name}", desc, json_content['spec'])

            source_file = os.path.join(os.getcwd(),
                                       self.setup.model_definition,
                                       "02-data",
                                       self.setup.dataset_name,
                                       f"*-{name}.csv.gz")
            for file in glob.glob(source_file):
                # ingest data with bundl/chunk
                for data_frm in pd.read_csv(file,
                                            sep=self.setup.csv_separator,
                                            header="infer",
                                            decimal=self.setup.csv_decimal,
                                            na_filter=False,
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




