"""
  TS701: Serving score from CART
"""

from qgate_sln_mlrun.ts.tsbase import TSBase


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

        # from pickle import load
        # from mlrun.execution import MLClientCtx
        # from mlrun.datastore import DataItem
        # from mlrun.artifacts import get_model, update_model
        # from mlrun.mlutils import eval_model_v2
        #
        # def test_model(context: MLClientCtx,
        #                models_path: DataItem,
        #                test_set: DataItem,
        #                label_column: str):
        #     if models_path is None:
        #         models_path = context.artifact_subpath("models")
        #     xtest = test_set.as_df()
        #     ytest = xtest.pop(label_column)
        #
        #     model_file, model_obj, _ = get_model(models_path)
        #     model = load(open(model_file, 'rb'))
        #
        #     extra_data = eval_model_v2(context, xtest, ytest.values, model)
        #     update_model(model_artifact=model_obj, extra_data=extra_data,
        #                  metrics=context.results, key_prefix='validation-')

