"""
  TS201: Create feature set(s)
"""
import datetime
from qgate_sln_mlrun.ts.tsbase import TSBase
import os
import json
import glob
from qgate_sln_mlrun.helper.featuresethelper import FeatureSetHelper


class TS201(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)
        self._fshelper = FeatureSetHelper(self._solution)

    @property
    def desc(self) -> str:
        return "Create feature set(s)"

    @property
    def long_desc(self):
        return ("Create feature set with name, description, entities, features and targets. "
                "Supported these targets off-line 'parquet', 'csv' and the on-line 'redis'.")

    def prj_exec(self, project_name):
        """ Get or create featuresets"""

        for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
            definition=self._fshelper.get_definition(project_name, featureset_name)
            if definition:
                self._create_featureset(f'{project_name}/{featureset_name}', project_name, definition)

    @TSBase.handler_testcase
    def _create_featureset(self, testcase_name, project_name, json_file, featureset_prefix=None):
        self._fshelper.create_featureset(project_name, json_file, featureset_prefix)
