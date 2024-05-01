"""
  TS206: Create feature set(s) & Ingest from Kafka source (one step)
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


class TS206(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)
        self._mysql = MySQLHelper(self.setup)

    @property
    def desc(self) -> str:
        return "Create feature set(s) & Ingest from Kafka source (one step)"

    @property
    def long_desc(self):
        return ("Create feature set(s) & Ingest from Kafka source (one step, without save and load featureset)")

    def exec(self, project_name):
        """ Create featuresets & ingest"""
        return

        # # It can be executed only in case that configuration is fine
        # if not self._mysql.configured:
        #     return
        #
        # for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
        #     # Create table only in case, that table does not exist
        #     if not self._mysql.table_exist(featureset_name):
        #         self._mysql.create_table(featureset_name)
        #
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
        #             self._create_featureset_ingest(f'{project_name}/{featureset_name}', project_name, featureset_name, json_file)

    @TSBase.handler_testcase
    def _create_featureset_ingest(self, testcase_name, project_name, featureset_name, json_file):
        json_content = json.load(json_file)
        name, desc, lbls, kind = TSBase.get_json_header(json_content)

        if kind == "feature-set":

            # create feature set based on the logic in TS201
            ts=ts201.TS201(self._solution)
            featureset=ts.create_featureset_content(project_name, f"{self.name}-{name}", desc, json_content['spec'])

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

