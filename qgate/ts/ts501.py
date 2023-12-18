"""
  TS501: Get data from off-line feature vector(s)
"""

from qgate.ts.tsbase import TSBase
from qgate.modelsolution import ModelSolution
from qgate.output import Output
from qgate.setup import Setup


class TS501(TSBase):

    def __init__(self, solution: ModelSolution, output: Output, setup: Setup=None):
        super().__init__(solution, output, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Get data from off-line feature vector(s)"

    @property
    def long_desc(self):
        return "Get data from off-line feature vector"

    def exec(self):
        self.solution.get_data_offline(self)

