"""
  TS401: Create feature vector(s)
"""

from qgate.ts.tsbase import TSBase
from qgate.modelsolution import ModelSolution
from qgate.output import Output
from qgate.setup import Setup
import mlrun
import mlrun.feature_store as fstore
import json
import glob
import os


class TS401(TSBase):

    def __init__(self, solution: ModelSolution, output: Output, setup: Setup=None):
        super().__init__(solution, output, self.__class__.__name__)
        self.setup=setup

    @property
    def desc(self) -> str:
        return "Create feature vector(s)"

    @property
    def long_desc(self):
        return "Create feature vectors as join of relevant feature sets"

    def exec(self):
        self.create_featurevector()

    def create_featurevector(self):
        # https://docs.mlrun.org/en/latest/api/mlrun.feature_store.html#mlrun.feature_store.FeatureVector

        self.testscenario_new()
        for project_name in self.solution._projects:
            for featurevector_name in self.get_featurevectors(self.solution._project_specs.get(project_name)):
                # create file with definition of vector
                source_file = os.path.join(os.getcwd(),
                                           self.setup.model_definition,
                                           "01-model",
                                           "03-feature-vector",
                                           f"*-{featurevector_name}.json")

                # check existing data set
                for file in glob.glob(source_file):
                    # iterate cross all featureset definitions
                    with open(file, "r") as json_file:
                        self._create_featurevector(f"{project_name}/{featurevector_name}", project_name, json_file)

    @TSBase.handler_testcase
    def _create_featurevector(self, testcase_name, project_name, json_file):
        json_content = json.load(json_file)
        name, desc, lbls, kind = self.get_json_header(json_content)

        if kind == "feature-vector":
            # create feature vector only in case not exist
            try:
                fstore.get_feature_vector(f"{project_name}/{name}")
            except:
                self._create_featurevector_content(project_name, name, desc, json_content['spec'])

    def _create_featurevector_content(self, project_name, featurevector_name, featurevector_desc, json_spec):
        # switch to proper project if the current project is different
        if mlrun.get_current_project().name != project_name:
            mlrun.load_project(name=project_name, context="./", user_project=False)

        features = json_spec['features']

        # create feature vector
        vector = fstore.FeatureVector(featurevector_name, features, description=featurevector_desc)
        vector.save()


