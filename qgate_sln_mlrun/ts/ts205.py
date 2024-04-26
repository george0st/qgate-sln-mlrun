"""
  TS205: Create feature set(s) & Ingest from SQL source (one step)
"""
from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore
from mlrun.data_types.data_types import ValueType
from mlrun.datastore.sources import SQLSource
from qgate_sln_mlrun.ts import ts201
import os
import json
import glob
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import sqlalchemy
import pymysql.cursors
from qgate_sln_mlrun.ts.tshelper import TSHelper


class TS205(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Create feature set(s) & Ingest from SQL source (one step)"

    @property
    def long_desc(self):
        return ("Create feature set(s) & Ingest from SQL (MySQL) source (one step, without save and load featureset)")

    def create_table(self,project_name, featureset_name):
        """Create table in MySQL"""
        primary_keys=""
        columns=""

        source_file = os.path.join(os.getcwd(),
                                   self.setup.model_definition,
                                   "01-model",
                                   "02-feature-set",
                                   f"*-{featureset_name}.json")

        for file in glob.glob(source_file):

            # iterate cross all featureset definitions
            with open(file, "r") as json_file:
                json_content = json.load(json_file)
                name, desc, lbls, kind = TSBase.get_json_header(json_content)

                # create SQL source based on the featureset
                json_spec=json_content['spec']

                # primary keys
                for item in json_spec['entities']:
                    columns+=f"{item['name']} {TSHelper.type_to_mysql_type(item['type'])},"
                    primary_keys+=f"{item['name']},"

                # columns
                for item in json_spec['features']:
                    columns+=f"{item['name']} {TSHelper.type_to_mysql_type(item['type'])},"

        table_name=f"src_{project_name}_{featureset_name}".replace('-','_')

        # connect
        user_name, password, host, port, db = TSHelper.split_sqlalchemy_connection(self.setup.mysql)
        connection = pymysql.connect(host=host,
                                     port=port,
                                     user=user_name,
                                     password=password,
                                     database=db,
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:

                # drop table
                cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
                connection.commit()

                # create table
                cursor.execute(f"CREATE TABLE {table_name} ({columns[:-1]}, PRIMARY KEY ({primary_keys[:-1]}));".replace('-','_'))
                connection.commit()

                # TODO: insert data

    def insert_into(self, project_name, featureset_name):
        """Insert data into table in MySQL"""
        pass

    def exec(self, project_name):
        """ Create featuresets & ingest"""
        for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
            self.create_table(project_name, featureset_name)

        # TODO: test, if mySQL is available
        pass
        # for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
        #     # create file with definition of vector
        #     source_file = os.path.join(os.getcwd(),
        #                                self.setup.model_definition,
        #                                "01-model",
        #                                "02-feature-set",
        #                                f"*-{featureset_name}.json")
        #
        #     for file in glob.glob(source_file):
        #         # iterate cross all featureset definitions
        #         with open(file, "r") as json_file:
        #             self._create_featureset_ingest(f'{project_name}/{featureset_name}', project_name, json_file)

    @TSBase.handler_testcase
    def _create_featureset_ingest(self, testcase_name, project_name, json_file):
        json_content = json.load(json_file)
        name, desc, lbls, kind = TSBase.get_json_header(json_content)

        if kind == "feature-set":

            # create feature set based on the logic in TS201
            ts=ts201.TS201(self._solution)
            featureset=ts.create_featureset_content(project_name, f"{self.name}-{name}", desc, json_content['spec'])

            source_file = os.path.join(os.getcwd(),
                                       self.setup.model_definition,
                                       "02-data",
                                       self.setup.dataset_name,
                                       f"*-{name}.parquet")
            for file in glob.glob(source_file):

                fstore.ingest(featureset,
                              SQLSource(name="tst", path=file),
                              # overwrite=False,
                              return_df=False,
                              # infer_options=mlrun.data_types.data_types.InferOptions.Null)
                              infer_options=mlrun.data_types.data_types.InferOptions.default())
                # TODO: use InferOptions.Null with python 3.10 or focus on WSL
                # NOTE: option default, change types
                # NOTE: option Null, generate error with datetime in python 3.9

