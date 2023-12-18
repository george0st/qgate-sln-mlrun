"""
  TS301: Ingest data to feature set(s)
"""

from qgate.ts.tsbase import TSBase
from qgate.modelsolution import ModelSolution
from qgate.output import Output
from qgate.setup import Setup


class TS301(TSBase):

    def __init__(self, solution: ModelSolution, output: Output, setup: Setup=None):
        super().__init__(solution, output, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Ingest data to feature set(s)"

    @property
    def long_desc(self):
        return "Ingest data to feature set from data source to targets based on feature set definition"

    def exec(self):
        self.solution.ingest_data(self)

