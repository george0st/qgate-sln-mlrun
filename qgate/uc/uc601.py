"""
  UC601: Serving score from CART
"""

from qgate.uc.ucbase import UCBase
from qgate.solution import Solution
from qgate.uc.ucoutput import UCOutput


class UC601(UCBase):

    def __init__(self, sln: Solution, output: UCOutput):
        super().__init__(sln, output, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Serving score from CART"

    @property
    def long_desc(self):
        return "Serving score from CART"

    def exec(self):
        self.sln.serving_score(self)

