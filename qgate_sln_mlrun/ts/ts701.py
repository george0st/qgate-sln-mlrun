"""
  TS701: Serving score from CART
"""

from qgate_sln_mlrun.ts.tsbase import TSBase


class TS601(TSBase):

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

        # Evaluating the Model
        pass


