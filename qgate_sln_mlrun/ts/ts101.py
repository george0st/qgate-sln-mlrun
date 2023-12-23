"""
  TS101: Create project(s)
"""
from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import os
import json
import glob


class TS101(TSBase):

    def __init__(self, solution):
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

        :param ts:      Test scenario
        """
        self.testscenario_new()
        dir=os.path.join(os.getcwd(), self.setup.model_definition, "01-model", "01-project", "*.json")
        for file in glob.glob(dir):
            with (open(file, "r") as json_file):
                json_content = json.load(json_file)
                name, desc, lbls, kind = self.get_json_header(json_content)

                #self.solution.projects.append(name)
                self.projects.append(name)
                if self._create_project(name, desc, lbls, kind):
                    #self.solution.project_specs[name] = json_content['spec']
                    self.project_specs[name] = json_content['spec']

    @TSBase.handler_testcase
    def _create_project(self, name, desc, lbls, kind):
        """Create project"""

        prj = mlrun.get_or_create_project(name, context="./", user_project=False)
        prj.description = desc
        for lbl in lbls:
            prj.metadata.labels[lbl] = lbls[lbl]
        prj.save()
        return True
