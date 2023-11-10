"""
  UC102: Delete project
"""

from qgate.uc.ucbase import UCBase


class UC102(UCBase):

    def __init__(self, environment):
        super().__init__(environment, self.__class__.__name__)

    def desc(self):
        return "Delete project"
