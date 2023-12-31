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

        vectors=None
        if self.test_setting.get('vector'):
            if self.test_setting['vector'].get('online'):
                vectors=self.test_setting['vector']['online']

        if vectors:
            for project_name in self.projects:
                for featurevector_name in self.get_featurevectors(self.project_specs.get(project_name)):
                    if featurevector_name in vectors:
                        self._get_data_online(f"{project_name}/{featurevector_name}", project_name, featurevector_name)

    @TSBase.handler_testcase
    def _get_data_online(self, testcase_name, project_name, featurevector_name):
        self.project_switch(project_name)
        vector = fstore.get_feature_vector(f"{project_name}/{featurevector_name}")

        with fstore.get_online_feature_service(vector) as svc:
            entities = [{"party-id": "d68fe603-7cb1-44e4-9013-7330a050a6be"}]
            resp=svc.get(entities, as_list=True)

