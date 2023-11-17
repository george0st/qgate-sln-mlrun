"""
  UC102: Delete project(s)
"""

from qgate.uc.ucbase import UCBase
from qgate.solution import Solution
from qgate.uc.ucoutput import UCOutput


class UC102(UCBase):

    def __init__(self, sln: Solution, output: UCOutput):
        super().__init__(sln, output, self.__class__.__name__)


    @property
    def desc(self) -> str:
        return "Delete project(s)"

    def long_desc(self):
        return "Delete project(s) include all content and targets"

    def exec(self):
        self.sln.delete_projects(self)

