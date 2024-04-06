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

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Ingest data to feature set(s) from Parquet source "

    @property
    def long_desc(self):
        return "Ingest data to feature set(s) from Parquet source"

    def prepare(self):
        # convert CSV to parquet
        # TODO: Add conversion
        pass

        # import pandas as pd
        # import pyarrow as pa
        # import pyarrow.parquet as pq
        #
        # csv_file_path = "./path/to/your/data.csv"
        # df = pd.read_csv(csv_file_path)
        #
        # table = pa.Table.from_pandas(df)
        #
        # parquet_file_path = "./path/to/your/data.parquet"
        # pq.write_table(table, parquet_file_path)

        # Pyarrow
        import pyarrow.parquet as pq
        import pyarrow.csv as pacsv

        # read
        parse_options = pacsv.ParseOptions(delimiter="\t", quote_char="^")
        arrow_table = pacsv.read_csv("csv_file", parse_options=parse_options)
        # Convert to Parquet
        pq.write_table(arrow_table, "parquet_file")

    def exec(self):
        #self.ingest_data()
        pass

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

        fstore.ingest(featureset,
                      ParquetSource(name="tst", path=file),
                      # overwrite=False,
                      return_df=False,
                      #infer_options=mlrun.data_types.data_types.InferOptions.Null)
                      infer_options=mlrun.data_types.data_types.InferOptions.default())
        # TODO: use InferOptions.Null with python 3.10 or focus on WSL
        # NOTE: option default, change types
        # NOTE: option Null, generate error with datetime in python 3.9




