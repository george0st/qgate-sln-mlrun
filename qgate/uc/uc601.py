"""
  UC601: Serving score from CART
"""

from qgate.uc.ucbase import UCBase
from qgate.solution import Solution
from qgate.uc.output_template import OutputTemplate


class UC601(UCBase):

    def __init__(self, sln: Solution, output: OutputTemplate):
        super().__init__(sln, output, self.__class__.__name__)

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

