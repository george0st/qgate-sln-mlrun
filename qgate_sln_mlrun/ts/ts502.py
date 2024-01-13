"""
  TS501: Get data from on-line feature vector(s)
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore
import os
import json


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

        #test
        test_featureset, test_entities, test_features=self._get_test_setting(featurevector_name)
        test_data=self._get_data_hint(featurevector_name, test_featureset)

        with fstore.get_online_feature_service(vector) as svc:
            # TODO add valid party-id from data
            entities = [{"party-id": "d68fe603-7cb1-44e4-9013-7330a050a6be"}]
            resp=svc.get(entities, as_list=True)

    def _get_test_setting(self,featurevector_name):
        test_detail=self.test_setting['vector']['test'][featurevector_name]

        test_featureset=test_detail['feature-set']
        test_entities=test_detail['entities']
        test_features=test_detail['features']
        return test_featureset, test_entities, test_features

    def _get_data_hint(self, featurevector_name, test_featureset):

        file = os.path.join(os.getcwd(),
                                   self.setup.model_definition,
                                   "03-test",
                                   f"{self.setup.dataset_name}.json")

        with open(file, "r") as json_file:
            json_content = json.load(json_file)
            name, desc, lbls, kind = TSBase.get_json_header(json_content)

        test_data=json_content['spec']['DataHint-0'][test_featureset]
        return test_data

