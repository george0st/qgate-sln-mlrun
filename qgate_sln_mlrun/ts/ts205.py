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
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import sqlalchemy
import pymysql.cursors
from qgate_sln_mlrun.ts.tshelper import TSHelper
from qgate_sln_mlrun.mysqlhelper import MySQLHelper


class TS205(TSBase):

#    TABLE_SOURCE_PREFIX = "tmp_"

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Create feature set(s) & Ingest from SQL source (one step)"

    @property
    def long_desc(self):
        return ("Create feature set(s) & Ingest from SQL (MySQL) source (one step, without save and load featureset)")

    # def create_sqlsource(self, featureset_name):
    #     """Create table in MySQL"""
    #     primary_keys=""
    #     column_types= ""
    #     columns = ""
    #
    #     source_file = os.path.join(os.getcwd(),
    #                                self.setup.model_definition,
    #                                "01-model",
    #                                "02-feature-set",
    #                                f"*-{featureset_name}.json")
    #
    #     for file in glob.glob(source_file):
    #
    #         # iterate cross all featureset definitions
    #         with open(file, "r") as json_file:
    #             json_content = json.load(json_file)
    #             name, desc, lbls, kind = TSBase.get_json_header(json_content)
    #
    #             # create SQL source based on the featureset
    #             json_spec=json_content['spec']
    #
    #             # primary keys
    #             for item in json_spec['entities']:
    #                 columns += f"{item['name']},"
    #                 column_types += f"{item['name']} {TSHelper.type_to_mysql_type(item['type'])},"
    #                 primary_keys += f"{item['name']},"
    #
    #             # columns
    #             for item in json_spec['features']:
    #                 columns += f"{item['name']},"
    #                 column_types+= f"{item['name']} {TSHelper.type_to_mysql_type(item['type'])},"
    #
    #     table_name = self._convert_feature_tablename(featureset_name)
    #     #f"{TS205.TABLE_SOURCE_PREFIX}{featureset_name}".replace('-','_')
    #     column_types = column_types[:-1].replace('-', '_')
    #     primary_keys = primary_keys[:-1].replace('-','_')
    #     columns = columns[:-1].replace('-', '_')
    #
    #     # connect
    #     user_name, password, host, port, db = TSHelper.split_sqlalchemy_connection(self.setup.mysql)
    #     connection = pymysql.connect(host=host,
    #                                  port=port,
    #                                  user=user_name,
    #                                  password=password,
    #                                  database=db,
    #                                  cursorclass=pymysql.cursors.DictCursor)
    #
    #     with connection:
    #         with connection.cursor() as cursor:
    #
    #             # drop table
    #             cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    #             connection.commit()
    #
    #             # create table
    #             #cursor.execute(f"CREATE TABLE {table_name} ({columns}, PRIMARY KEY ({primary_keys}));")
    #             cursor.execute(f"CREATE TABLE {table_name} ({column_types});")
    #             connection.commit()
    #
    #             # insert data
    #             self._insert_into(connection, cursor, table_name, featureset_name, columns)
    #
    # def _insert_into(self, connection, cursor, table_name, featureset_name, columns):
    #     """Insert data into table in MySQL"""
    #
    #     # create possible file for load
    #     source_file = os.path.join(os.getcwd(),
    #                                self.setup.model_definition,
    #                                "02-data",
    #                                self.setup.dataset_name,
    #                                f"*-{featureset_name}.csv.gz")
    #
    #     for file in glob.glob(source_file):
    #         # ingest data with bundl/chunk
    #         for data_frm in pd.read_csv(file,
    #                                     sep=self.setup.csv_separator,  # ";",
    #                                     header="infer",
    #                                     decimal=self.setup.csv_decimal,  # ",",
    #                                     compression="gzip",
    #                                     encoding="utf-8",
    #                                     chunksize=10000):
    #             for row in data_frm.to_numpy().tolist():
    #                 values=f"\",\"".join(str(e) for e in row)
    #
    #                 cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES(\"{values}\");")
    #             connection.commit()

    def after(self):
        # delete all tables with prefix TS205.TABLE_SOURCE_PREFIX
        # delete in TS102, not here
        pass

    # def _convert_feature_tablename(self, featureset_name):
    #     """Convert featureset name to the name of table."""
    #     return f"{TS205.TABLE_SOURCE_PREFIX}{featureset_name}".replace('-', '_')

    # def _mysql_table_exist(self, table_name):
    #     """Check, if table in MySQL exist
    #
    #     :param table_name:      name of the table for check
    #     :return:                True - table exist, False - table does not exist
    #     """
    #     user_name, password, host, port, db = TSHelper.split_sqlalchemy_connection(self.setup.mysql)
    #     connection = pymysql.connect(host=host,
    #                                  port=port,
    #                                  user=user_name,
    #                                  password=password,
    #                                  database=db,
    #                                  cursorclass=pymysql.cursors.DictCursor)
    #
    #     with connection:
    #         with connection.cursor() as cursor:
    #             cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = {db} AND table_name = {table_name} LIMIT 1;")
    #             myresult = cursor.fetchone()
    #             if myresult:
    #                 if len(myresult)>0:
    #                     return True
    #     return False

    def exec(self, project_name):
        """ Create featuresets & ingest"""

        mysql= MySQLHelper(self.setup)

        # It can be executed only in case that configuration is fine
        if not mysql.configured:
            return

        for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
            # Create table only in case, that table does not exist
            if not mysql.table_exist(featureset_name):
                mysql.create_table(featureset_name)

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

