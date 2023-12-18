"""
  TS401: Create feature vector(s)
"""

from qgate.ts.tsbase import TSBase
from qgate.solution import Solution
from qgate.output import Output
from qgate.setup import Setup


class TS401(TSBase):

    def __init__(self, sln: Solution, output: Output, setup: Setup=None):
        super().__init__(sln, output, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Create feature vector(s)"

    @property
    def long_desc(self):
        return "Create feature vectors as join of relevant feature sets"

    def exec(self):
        self.sln.create_featurevector(self)

