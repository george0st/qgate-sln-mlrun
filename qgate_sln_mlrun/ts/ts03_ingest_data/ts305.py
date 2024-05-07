"""
  TS305: Ingest data to feature set(s) from SQL source
"""


from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore
from mlrun.data_types.data_types import spark_to_value_type
from mlrun.datastore.sources import SQLSource
import glob
import os
from qgate_sln_mlrun.helper.mysqlhelper import MySQLHelper


class TS305(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)
        self._mysql = MySQLHelper(self.setup)

    @property
    def desc(self) -> str:
        return "Ingest data to feature set(s) from SQL source"

    @property
    def long_desc(self):
        return "Create feature set(s) & Ingest from SQL (MySQL) source"

    def prj_exec(self, project_name):
        """ Create featuresets & ingest"""

        # It can be executed only in case that configuration is fine
        if not self._mysql.configured:
            return

        for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
            # Create table only in case, that table does not exist
            if not self._mysql.table_exist(featureset_name):
                self._mysql.create_insert_data(featureset_name)

            # create file with definition of vector
            source_file = os.path.join(os.getcwd(),
                                       self.setup.model_definition,
                                       "01-model",
                                       "02-feature-set",
                                       f"*-{featureset_name}.json")

            for file in glob.glob(source_file):
                # iterate cross all featureset definitions
                with open(file, "r") as json_file:
                    self._create_featureset_ingest(f'{project_name}/{featureset_name}', project_name, featureset_name, json_file)

    @TSBase.handler_testcase
    def _create_featureset_ingest(self, testcase_name, project_name, featureset_name, json_file):

        featureset = fstore.get_feature_set(f"{project_name}/{featureset_name}")

        keys = ""
        for entity in featureset.spec.entities:
            keys+=f"{entity.name},"

        fstore.ingest(featureset,
                      SQLSource(name="tst",
                                table_name=self._mysql.convert_feature_tablename(featureset_name),
                                db_url=self.setup.mysql,
                                key_field=keys[:-1].replace('-','_')),
                      # overwrite=False,
                      return_df=False,
                      # infer_options=mlrun.data_types.data_types.InferOptions.Null)
                      infer_options=mlrun.data_types.data_types.InferOptions.default())
        # TODO: use InferOptions.Null with python 3.10 or focus on WSL
        # NOTE: option default, change types
        # NOTE: option Null, generate error with datetime in python 3.9

