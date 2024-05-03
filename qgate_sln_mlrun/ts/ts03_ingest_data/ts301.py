"""
  TS301: Ingest data (Preview mode)
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
from qgate_sln_mlrun.setup import Setup
import mlrun.feature_store as fstore
import pandas as pd
import glob
import os


class TS301(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Ingest data (Preview mode)"

    @property
    def long_desc(self):
        return "Ingest data (in Preview mode) from DataFrame Source"

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

    @TSBase.handler_testcase
    def _ingest_data(self, testcase_name, project_name, featureset_name, file):
        # get existing feature set (feature set have to be created in previous test scenario)
        featureset = fstore.get_feature_set(f"{project_name}/{featureset_name}")

        # ingest data with bundl/chunk
        for data_frm in pd.read_csv(file,
                                    sep=self.setup.csv_separator,
                                    header="infer",
                                    decimal=self.setup.csv_decimal,
                                    compression="gzip",
                                    encoding="utf-8",
                                    chunksize=Setup.MIN_BUNDLE):
            featureset.preview(data_frm)

