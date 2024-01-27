"""
  TS601: Build CART model
"""
from sklearn.preprocessing import LabelEncoder

from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun.feature_store as fstore
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import os
import glob
import json


class TS601(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Build CART model"

    @property
    def long_desc(self):
        """
        Long description, more information see these sources:
         - https://www.datacamp.com/tutorial/decision-tree-classification-python
         - https://scikit-learn.org/stable/modules/tree.html
        """
        return "Build CART model (Classification and Regression Tree) from Scikit-Learn"

    def exec(self):
        self.build_model()

    def build_model(self):

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
                        self._create_mlmodel(f"{project_name}/{mlmodel_name}", project_name, json_file)

    @TSBase.handler_testcase
    def _create_mlmodel(self, testcase_name, project_name, json_file):
        json_content = json.load(json_file)
        name, desc, lbls, kind = TSBase.get_json_header(json_content)

        if kind == "ml-model":

            # load data
            vector = fstore.get_feature_vector(f"{project_name}/{json_content['spec']['vector']}")
            resp = fstore.get_offline_features(vector)
            frm = resp.to_dataframe()

            # encoding
            labelencoder = LabelEncoder()
            for column in json_content["spec"]["encode"]:
                frm[column]=labelencoder.fit_transform(frm[column])

            # feature selection
            source=json_content["spec"]["source"]
            target=json_content["spec"]["target"]
            X=frm[source]
            y=frm[target]

            # split data
            X_train, X_test, y_train, y_test = train_test_split(X,
                                                                y,
                                                                test_size=json_content["spec"]["test-size"],
                                                                random_state=1)

            # train
            clf = DecisionTreeClassifier()
            clf = clf.fit(X_train, y_train)

            # predict
            y_pred = clf.predict(X_test)

            # store the model

            # from pickle import dumps
            # model_data = dumps(clf)
            # context.log_model(key='my_model', body=model_data, model_file='my_model.pkl')
