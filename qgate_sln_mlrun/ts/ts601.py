"""
  TS601: Build CART model
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun.feature_store as fstore
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
import os


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

        # Get list of models
        self.testscenario_new()
        for project_name in self.projects:
            for mlmodel_name in self.get_mlmodel(self.project_specs.get(project_name)):
                self._get_mlmodel(f"{project_name}/{mlmodel_name}", project_name, mlmodel_name)


        # Feature selection
        # feature_cols = ['pregnant', 'insulin', 'bmi', 'age', 'glucose', 'bp', 'pedigree']
        # X = pima[feature_cols]  # Features
        # y = pima.label  # Target variable

        # Split data

        # Building Decision Tree Model
        pass

    @TSBase.handler_testcase
    def _get_mlmodel(self, testcase_name, project_name, featurevector_name):
        pass