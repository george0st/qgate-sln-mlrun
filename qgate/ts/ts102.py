"""
  TS102: Delete project(s)
"""

from qgate.ts.tsbase import TSBase
from qgate.solution import Solution
from qgate.output import Output
from qgate.setup import Setup



class TS102(TSBase):

    def __init__(self, solution: Solution, output: Output, setup: Setup=None):
        super().__init__(solution, output, self.__class__.__name__)


    @property
    def desc(self) -> str:
        return "Delete project(s)"

    @property
    def long_desc(self):
        return "Delete project include all contents and targets (such as Parquet files, etc.)"

    def exec(self):
        self.sln.delete_projects(self)

