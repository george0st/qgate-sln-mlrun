"""
  TS601: Serving score from CART
"""

from qgate.ts.tsbase import TSBase
from qgate.solution import Solution
from qgate.output import Output
from qgate.setup import Setup


class TS601(TSBase):

    def __init__(self, solution: Solution, output: Output, setup: Setup=None):
        super().__init__(solution, output, self.__class__.__name__)

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
        self.sln.serving_score(self)

