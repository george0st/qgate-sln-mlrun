"""
  TS102: Delete project(s)
"""

from qgate.uc.tsbase import TSBase
from qgate.solution import Solution
from qgate.output import Output


class TS102(TSBase):

    def __init__(self, sln: Solution, output: Output):
        super().__init__(sln, output, self.__class__.__name__)


    @property
    def desc(self) -> str:
        return "Delete project(s)"

    @property
    def long_desc(self):
        return "Delete project include all contents and targets (such as Parquet files, etc.)"

    def exec(self):
        self.sln.delete_projects(self)
