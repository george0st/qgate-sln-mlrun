"""
  TS102: Delete project(s)
"""

from qgate.ts.tsbase import TSBase
from qgate.modelsolution import ModelSolution
from qgate.output import Output
import mlrun
import os
import json
import glob
import shutil



class TS102(TSBase):

    def __init__(self, solution: ModelSolution, output: Output):
        super().__init__(solution, output, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Delete project(s)"

    @property
    def long_desc(self):
        return "Delete project include all contents and targets (such as Parquet files, etc.)"

    def exec(self):
        #self.solution.delete_projects(self)
        self.delete_projects()

    def delete_projects(self):
        """Delete projects

        :param ts:      Test scenario
        """
        self.testscenario_new()
        for project_name in self.solution.projects:
            self._delete_project(project_name)

        # cleaning/delete other things in output directory (generated from e.g. CSVTargets)
        dir = os.path.join(os.getcwd(), self.setup.model_output, "*")
        for file in glob.glob(dir):
            if os.path.isdir(file):
                shutil.rmtree(file, True)

    @TSBase.handler_testcase
    def _delete_project(self, name):
        """Delete project"""
        mlrun.get_run_db().delete_project(name, "cascade")

        # delete project in FS
        project_dir = os.path.join(self.setup.model_output, name)
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir, True)
