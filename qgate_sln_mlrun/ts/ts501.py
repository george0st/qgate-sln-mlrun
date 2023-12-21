"""
  TS501: Get data from off-line feature vector(s)
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
from qgate_sln_mlrun.modelsolution import ModelSolution
from qgate_sln_mlrun.output import Output
from qgate_sln_mlrun.modelsetup import ModelSetup
import mlrun
import mlrun.feature_store as fstore
import json
import glob
import os


class TS501(TSBase):

    def __init__(self, solution: ModelSolution, output: Output):
        super().__init__(solution, output, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Get data from off-line feature vector(s)"

    @property
    def long_desc(self):
        return "Get data from off-line feature vector"

    def exec(self):
        self.get_data_offline()

    def get_data_offline(self):
        """
        Get data from off-line feature vector
        """
        self.testscenario_new()
        for project_name in self.solution.projects:
            for featurevector_name in self.get_featurevectors(self.solution.project_specs.get(project_name)):
                self._get_data_offline(f"{project_name}/{featurevector_name}", project_name, featurevector_name)


    @TSBase.handler_testcase
    def _get_data_offline(self, testcase_name, project_name, featurevector_name):
        self.project_switch(project_name)
        vector = fstore.get_feature_vector(f"{project_name}/{featurevector_name}")

        resp = fstore.get_offline_features(vector)
        frm = resp.to_dataframe()
        self.testcase_detail(f"... get {len(frm.index)} items")


