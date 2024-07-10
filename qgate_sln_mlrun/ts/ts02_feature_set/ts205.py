"""
  TS205: Create feature set(s) & Ingest from SQL source (one step)
"""
from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore
from mlrun.data_types.data_types import ValueType
from mlrun.datastore.sources import SQLSource
import os
import json
import glob
from qgate_sln_mlrun.helper.mysqlhelper import MySQLHelper
from qgate_sln_mlrun.helper.featuresethelper import FeatureSetHelper


class TS205(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)
        self._mysql = MySQLHelper(self.setup)
        self._fshelper = FeatureSetHelper(self._solution)

    @property
    def desc(self) -> str:
        return "Create feature set(s) & Ingest from SQL source (one step)"

    @property
    def long_desc(self):
        return ("Create feature set(s) & Ingest from SQL (MySQL) source (one step, without save and load featureset)")

    def prj_exec(self, project_name):
        """ Create featuresets & ingest"""

        # It can be executed only in case that configuration is fine
        if not self._mysql.configured:
            return

        for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
            # Create table as data source
            self._mysql.create_insert_data(self._mysql.create_helper(featureset_name), featureset_name, False)

            # Get definition for featureset
            definition = self._fshelper.get_definition(project_name, featureset_name)
            if definition:
                self._create_featureset(f'{project_name}/{featureset_name}', project_name, featureset_name, definition, self.name)

    @TSBase.handler_testcase
    def _create_featureset(self, testcase_name, project_name, featureset_name, definition, featureset_prefix=None):
        # Create feature set
        featureset = self._fshelper.create_featureset(project_name, definition, featureset_prefix)

        keys = ""
        for entity in featureset.spec.entities:
            keys+=f"{entity.name},"

        fstore.ingest(featureset,
                      SQLSource(name="tst",
                                table_name=self._mysql.create_helper(featureset_name),
                                db_url=self.setup.mysql,
                                key_field=keys[:-1].replace('-','_')),
                      # overwrite=False,
                      return_df=False,
                      #infer_options=mlrun.data_types.data_types.InferOptions.Null)
                      infer_options=mlrun.data_types.data_types.InferOptions.default())
        # TODO: use InferOptions.Null with python 3.10 or focus on WSL
        # NOTE: option default, change types
        # NOTE: option Null, generate error with datetime in python 3.9

