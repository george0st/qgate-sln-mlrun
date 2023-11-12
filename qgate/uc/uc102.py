"""
  UC102: Delete project
"""

from qgate.uc.ucbase import UCBase
from qgate.solution import Solution


class UC102(UCBase):

    def __init__(self, sln: Solution):
        super().__init__(sln, self.__class__.__name__)

    def desc(self):
        return "Delete project(s)"

    def exec(self):
        self.sln.delete_projects()
