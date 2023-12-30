"""
  TS501: Get data from on-line feature vector(s)
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore


class TS502(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Get data from on-line feature vector(s)"

    @property
    def long_desc(self):
        return "Get data from on-line feature vector"

    def exec(self):
        self.get_data_online()

    def get_data_online(self):
        """
        Get data from on-line feature vector
        """
        self.testscenario_new()
        for project_name in self.projects:
            for featurevector_name in self.get_featurevectors(self.project_specs.get(project_name)):
                self._get_data_online(f"{project_name}/{featurevector_name}", project_name, featurevector_name)


    @TSBase.handler_testcase
    def _get_data_online(self, testcase_name, project_name, featurevector_name):
        self.project_switch(project_name)
        vector = fstore.get_feature_vector(f"{project_name}/{featurevector_name}")

        svc=fstore.get_online_feature_service(vector)
        # Define the wanted entities
        entities = [{"source": 1}]
        # Get the feature vectors from the service
        resp=svc.get(entities,as_list=True)
        self.testcase_detail(f"... get xxx items")
