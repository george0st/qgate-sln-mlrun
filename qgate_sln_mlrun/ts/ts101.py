"""
  TS101: Create project(s)
"""
from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import os
import json
import glob


class TS101(TSBase):

    def __init__(self, solution, setting: dict[str, object]=None):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Create project(s)"

    @property
    def long_desc(self):
        return "Create project with setting name, description and tags"

    def exec(self):
        self.create_projects()

    def create_projects(self):
        """ Create projects based on json definition
        """
        self.testscenario_new()
        for project_name in self.projects:
            desc = self.project_descs[project_name]
            self._create_project(f"{project_name}/*: '{desc[0]}'", project_name, desc[0], desc[1], desc[2])

    @TSBase.handler_testcase
    def _create_project(self, testcase_name, name, desc, lbls, kind):
        """Create project"""

        prj = mlrun.get_or_create_project(name, context=os.path.join(self.setup.model_output, name), user_project=False, save=False)
        prj.description = desc
        for lbl in lbls:
            prj.metadata.labels[lbl] = lbls[lbl]
        prj.save()
        return True
