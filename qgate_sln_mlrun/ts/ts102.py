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
        """Delete projects and addition content of output directory"""
        self.testscenario_new()
        for project_name in self.projects:
            self._delete_project(f"{project_name}/*:", project_name)

        # not remove files from today
        # (this line generate file profix for today)
        not_remove = f"qgt-mlrun-{str.replace(self.output.datetime, ':', '-')}".split(" ")[0]

        # cleaning/delete other directories in output directory (generated from e.g. CSVTargets)
        dir = os.path.join(os.getcwd(), self.setup.model_output, "*")
        for file in glob.glob(dir):
            if os.path.isdir(file):
                shutil.rmtree(file, True)
            # remove old files (d-1 and olders) from templates "qgt-mlrun-*"
            elif not os.path.basename(file).startswith(not_remove):
                os.remove(file)


    @TSBase.handler_testcase
    def _delete_project(self, label, name):
        """Delete project (in MLRun and in file system)"""

        # if full delete, delete project in MLRun also
        if self.setup.get_scenario_setting("TS102_DELETE") == ProjectDelete.FULL_DELETE:
            mlrun.get_run_db().delete_project(name, "cascade") #mlrun.common.schemas.DeletionStrategy.cascade)

        # delete directory with the same name as project in FS (valid for partly delete)
        project_dir = os.path.join(self.setup.model_output, name)
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir, True)
