"""
  TS701: Serving score from CART
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
from pickle import load
from mlrun.datastore import DataItem
from mlrun.artifacts import get_model, update_model
import os
import glob
import json

class TS701(TSBase):

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
        #     if models_path is None:
        #         models_path = context.artifact_subpath("models")
        #     xtest = test_set.as_df()
        #     ytest = xtest.pop(label_column)
            models_path="C:\Python\qgate-sln-mlrun\output\0\model-transaction\model-transaction.pkl"
            #store://models/gate-alfa/output_model-transaction#0:latest
            model_file, model_artifact, extra_data = get_model(models_path, suffix='.pkl')
            model = load(open(model_file, "rb"))
            categories = extra_data['categories'].as_df()

        #
        #     extra_data = eval_model_v2(context, xtest, ytest.values, model)
        #     update_model(model_artifact=model_obj, extra_data=extra_data,
        #                  metrics=context.results, key_prefix='validation-')

