"""
  TS101: Create project(s)
"""
from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import os


class TS101(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Create project(s)"

    @property
    def long_desc(self):
        return "Create project with requested name, description and tags"

    def prj_exec(self, project_name):
        """ Create projects based on json definition"""
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
