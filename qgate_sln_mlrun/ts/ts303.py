"""
  TS303: Ingest data to feature set(s) from Parquet Source
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore
from mlrun.data_types.data_types import spark_to_value_type
from mlrun.datastore.sources import ParquetSource
import pandas as pd
import glob
import os


class TS303(TSBase):

    def __init__(self, solution, setting: dict[str,str]=None):
        super().__init__(solution, self.__class__.__name__)
        self._temp=os.path.join(self.setup.model_output,"temp")
        if not os.path.exists(self._temp):
            os.makedirs(self._temp)

    @property
    def desc(self) -> str:
        return "Ingest data to feature set(s) from Parquet source "

    @property
    def long_desc(self):
        return "Ingest data to feature set(s) from Parquet source"

    def _cvs_to_parquest(self, csv_file) -> str:
        import pyarrow.parquet as pq
        import pyarrow.csv as pacsv

        # csv setting
        parse_options = pacsv.ParseOptions(delimiter=self.setup.csv_separator)
        convert_options = pacsv.ConvertOptions(decimal_point=self.setup.csv_decimal)

        # read csv
        arrow_table = pacsv.read_csv(csv_file, parse_options=parse_options, convert_options=convert_options)

        # write parquet
        file_name = os.path.basename(os.path.basename(csv_file))
        parquet_file=os.path.join(self._temp, f"{file_name.split('.')[0]}.parquet")
        pq.write_table(arrow_table, parquet_file)
        return parquet_file

    def exec(self):
        self.ingest_data()

    def ingest_data(self):
        """Data ingest
        """
        self.testscenario_new()
        for project_name in self.projects:
            for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
                # create possible file for load
                source_file=os.path.join(os.getcwd(),
                                         self.setup.model_definition,
                                         "02-data",
                                         self.setup.dataset_name,
                                         f"*-{featureset_name}.csv.gz")

                # check existing data set
                for file in glob.glob(source_file):
                    self._ingest_data( f"{project_name}/{featureset_name}", project_name, featureset_name, file)

    @TSBase.handler_testcase
    def _ingest_data(self, testcase_name, project_name, featureset_name, file):
        # get existing feature set (feature set have to be created in previous test scenario)
        featureset = fstore.get_feature_set(f"{project_name}/{featureset_name}")

        # create parquest file from csv
        parquet_file=self._cvs_to_parquest(file)

        fstore.ingest(featureset,
                      ParquetSource(name="tst", path=parquet_file),
                      # overwrite=False,
                      return_df=False,
                      #infer_options=mlrun.data_types.data_types.InferOptions.Null)
                      infer_options=mlrun.data_types.data_types.InferOptions.default())
        # TODO: use InferOptions.Null with python 3.10 or focus on WSL
        # NOTE: option default, change types
        # NOTE: option Null, generate error with datetime in python 3.9




