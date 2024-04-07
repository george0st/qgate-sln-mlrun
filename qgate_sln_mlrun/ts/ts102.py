"""
  TS102: Delete project(s)
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import os
import glob
import shutil
from qgate_sln_mlrun.setup import ProjectDelete


class TS102(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Delete project(s)"

    @property
    def long_desc(self):
        return "Delete project include all contents and targets (such as Parquet/CSV files, etc.)"

    def exec(self):
        self.delete_projects()

    def delete_projects(self):
        """Delete projects
        """
        self.testscenario_new()
        for project_name in self.projects:
            self._delete_project(f"{project_name}/*:", project_name)

        # cleaning/delete other things in output directory (generated from e.g. CSVTargets)
        dir = os.path.join(os.getcwd(), self.setup.model_output, "*")
        for file in glob.glob(dir):
            if os.path.isdir(file):
                shutil.rmtree(file, True)

    @TSBase.handler_testcase
    def _delete_project(self, label, name):
        """Delete project (include MLRun, file system, etc.)"""

        # if full delete
        if self.setup.get_scenario_setting("TS102_DELETE") == ProjectDelete.FULL_DELETE:
            mlrun.get_run_db().delete_project(name, "cascade") #mlrun.common.schemas.DeletionStrategy.cascade)

        # if partly delete
        # delete project in FS
        project_dir = os.path.join(self.setup.model_output, name)
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir, True)
