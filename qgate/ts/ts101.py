"""
  TS101: Create project(s)
"""

from qgate.ts.tsbase import TSBase
from qgate.output import Output
from qgate.modelsolution import ModelSolution
import mlrun
import os
import json
import glob
from qgate.setup import Setup


class TS101(TSBase):

    def __init__(self, solution: ModelSolution, output: Output, setup: Setup=None):
        super().__init__(solution, output, self.__class__.__name__)
        self.setup=setup


    @property
    def desc(self) -> str:
        return "Create project(s)"

    @property
    def long_desc(self):
        return "Create project with setting name, description and tags"

    def exec(self):
        self.create_projects(self)
        #self.sln.create_projects(self)

    def create_projects(self, ts: TSBase):
        """ Create projects based on json definition

        :param ts:      Test scenario
        """
        ts.testscenario_new()
        dir=os.path.join(os.getcwd(), self.setup.model_definition, "01-model", "01-project", "*.json")
        for file in glob.glob(dir):
            with (open(file, "r") as json_file):
                json_content = json.load(json_file)
                name, desc, lbls, kind = self.get_json_header(json_content)

                self.solution._projects.append(name)
                if self._create_project(ts, name, desc, lbls, kind):
                    self.solution._project_specs[name] = json_content['spec']

    @TSBase.handler_testcase
    def _create_project(self, ts: TSBase, name, desc, lbls, kind):
        """Create project"""

        prj = mlrun.get_or_create_project(name, context="./", user_project=False)
        prj.description = desc
        for lbl in lbls:
            prj.metadata.labels[lbl] = lbls[lbl]
        prj.save()
        return True


