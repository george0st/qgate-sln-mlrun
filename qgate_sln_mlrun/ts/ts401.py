"""
  TS401: Create feature vector(s)
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore
import json
import glob
import os


class TS401(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

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
        for project_name in self.projects:
            for featurevector_name in self.get_featurevectors(self.project_specs.get(project_name)):
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
        name, desc, lbls, kind = TSBase.get_json_header(json_content)

        if kind == "feature-vector":
            # create feature vector only in case not exist
            try:
                fstore.get_feature_vector(f"{project_name}/{name}")
            except:
                self._create_featurevector_content(project_name, name, desc, json_content['spec'])

    def _create_featurevector_content(self, project_name, featurevector_name, featurevector_desc, json_spec):

        self.project_switch(project_name)
        features = json_spec['features']

        # create feature vector
        vector = fstore.FeatureVector(featurevector_name, features, description = featurevector_desc, with_indexes = True)
        vector.save()


