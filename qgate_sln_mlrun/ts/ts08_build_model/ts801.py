"""
  TS801: Build CART model (based on off-line feature vector)
"""
from sklearn.preprocessing import LabelEncoder
from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun.feature_store as fstore
import mlrun
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import os
import glob
import json
from pickle import dumps


class TS801(TSBase):

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

    def prj_exec(self, project_name):

        # Get list of ml models
        for mlmodel_name in self.get_mlmodel(self.project_specs.get(project_name)):
            source_file = os.path.join(os.getcwd(),
                                       self.setup.model_definition,
                                       "01-model",
                                       "05-ml-model",
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
            vector = fstore.get_feature_vector(f"{project_name}/{json_content['spec']['source']}")
            resp = vector.get_offline_features()
            frm = resp.to_dataframe()

            # encode data
            labelencoder = LabelEncoder()
            for column in json_content["spec"]["encode-columns"]:
                frm[column]=labelencoder.fit_transform(frm[column])

            # select data for training
            X=frm[json_content["spec"]["source-columns"]]
            y=frm[json_content["spec"]["target-columns"]]

            # split data
            X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                                test_size=json_content["spec"]["test-size"],
                                                                random_state=1)

            # train
            clf = DecisionTreeClassifier()
            clf = clf.fit(X_train, y_train)

            # predict
            # y_pred = clf.predict(X_test)

            # store the model
            model_data = dumps(clf)
            context = mlrun.get_or_create_ctx(name="output", with_env=False, project=project_name)
            #context.log_artifact(f"aa-{name}",body=model_data,local_path=f'aa-{name}.pkl')
            context.log_model(key=name,
                              body=model_data,
                              model_dir="/".join([self.setup.model_output, project_name]),
                              model_file=f'{name}.pkl')
