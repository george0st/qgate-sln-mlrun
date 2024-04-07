"""
  TS801: Serving score from CART
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
from pickle import load
from mlrun.datastore import DataItem
from mlrun.artifacts import get_model, update_model
import mlrun
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import mlrun.feature_store as fstore
from sklearn.preprocessing import LabelEncoder
import os
import glob
import json

class TS801(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Serving score from CART"

    @property
    def long_desc(self):
        """
        Long description, more information see these sources:
         - https://www.datacamp.com/tutorial/decision-tree-classification-python
         - https://scikit-learn.org/stable/modules/tree.html
        """
        return "Serving score from CART (Classification and Regression Tree) from Scikit-Learn"

    def exec(self):
        self.serving_score()

    def serving_score(self):
        """
        Serve score
        """
        # Get list of ml models
        self.testscenario_new()
        for project_name in self.projects:
            for mlmodel_name in self.get_mlmodel(self.project_specs.get(project_name)):
                source_file = os.path.join(os.getcwd(),
                                           self.setup.model_definition,
                                           "01-model",
                                           "04-ml-model",
                                           f"*-{mlmodel_name}.json")

                # check existing data set
                for file in glob.glob(source_file):
                    # iterate cross all ml models definitions
                    with open(file, "r") as json_file:
                        self._use_mlmodel(f"{project_name}/{mlmodel_name}", project_name, json_file)

    @TSBase.handler_testcase
    def _use_mlmodel(self, testcase_name, project_name, json_file):
        json_content = json.load(json_file)
        name, desc, lbls, kind = TSBase.get_json_header(json_content)

        if kind == "ml-model":

            # get data
            vector = fstore.get_feature_vector(f"{project_name}/{json_content['spec']['source']}")
            resp = vector.get_offline_features()
            frm = resp.to_dataframe()

            # encode data
            labelencoder = LabelEncoder()
            for column in json_content["spec"]["encode-columns"]:
                frm[column] = labelencoder.fit_transform(frm[column])

            # select data for prediction
            X = frm[json_content["spec"]["source-columns"]]

            # get model
            context = mlrun.get_or_create_ctx("output", project=project_name)
            for artifact in context.artifacts:
                if artifact['kind']=='model' and artifact['metadata']['key']=='model-transaction':
                    models_path=artifact['spec']['target_path']
            model_file, model_artifact, extra_data = get_model(models_path, suffix='.pkl')
            model = load(open(model_file, "rb"))

            # predict
            model.predict(X)
