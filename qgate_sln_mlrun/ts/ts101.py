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
        """
        self.testscenario_new()
        dir=os.path.join(os.getcwd(), self.setup.model_definition, "01-model", "01-project", "**", "*.json")
        for file in glob.glob(dir, recursive=True):
            with (open(file, "r") as json_file):
                json_content = json.load(json_file)
                name, desc, lbls, kind, parent = TSBase.get_json_header_full(json_content)

                # add project include project inheritance
                self.projects.append(name)
                self.project_specs[name] = json_content['spec']
                self._add_inheritance(name, parent)

                self._create_project(name, desc, lbls, kind)

    def _add_inheritance(self, project_name, parent):
        """Copy 'spec' content from parent project, but only for missing items"""
        if parent:
            for spec_item in self.project_specs[parent]:
                itm=self.project_specs[project_name].get(spec_item, None)
                if itm is None:
                    self.project_specs[project_name][spec_item]=self.project_specs[parent][spec_item]

    @TSBase.handler_testcase
    def _create_project(self, name, desc, lbls, kind):
        """Create project"""

        prj = mlrun.get_or_create_project(name, context=self.setup.model_output, user_project=False, save=False)
        prj.description = desc
        for lbl in lbls:
            prj.metadata.labels[lbl] = lbls[lbl]
        prj.save()
        return True
