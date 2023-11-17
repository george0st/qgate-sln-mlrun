"""
  UC101: Create project(s)
"""

import mlrun
from qgate.uc.ucbase import UCBase
from qgate.uc.ucsetup import UCSetup
from qgate.uc.ucoutput import UCOutput
from qgate.solution import Solution
import os
import glob
import json


class UC101(UCBase):

    def __init__(self, sln: Solution, output: UCOutput):
        super().__init__(sln, output, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Create project(s)"

    def long_desc(self):
        return "Create project(s) with setting name, desription and tags"

    def exec(self):
        self.sln.create_projects(self)

