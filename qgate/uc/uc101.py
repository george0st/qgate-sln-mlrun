"""
  UC101: Create project
"""

import mlrun
from qgate.uc.ucbase import UCBase
from qgate.uc.ucsetup import UCSetup
from qgate.solution import Solution
import os
import glob
import json


class UC101(UCBase):

    def __init__(self, sln: Solution):
        super().__init__(sln, self.__class__.__name__)

    @property
    def desc(self):
        return "Create project(s)"

    def exec(self):
        self.sln.create_projects()

