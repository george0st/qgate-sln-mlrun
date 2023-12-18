"""
  TS201: Create feature set(s)
"""

from qgate.ts.tsbase import TSBase
from qgate.solution import Solution
from qgate.output import Output
from qgate.setup import Setup


class TS201(TSBase):

    def __init__(self, solution: Solution, output: Output, setup: Setup=None):
        super().__init__(solution, output, self.__class__.__name__)


    @property
    def desc(self) -> str:
        return "Create feature set(s)"

    @property
    def long_desc(self):
        return "Create feature set with name, description, entities, features and targets"

    def exec(self):
        self.sln.create_featuresets(self)

