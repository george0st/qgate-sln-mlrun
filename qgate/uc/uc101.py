"""
  UC101: Create project
"""

from qgate.uc.ucbase import UCBase


class UC101(UCBase):

    def __init__(self, environment):
        super().__init__(environment, self.__class__.__name__)

