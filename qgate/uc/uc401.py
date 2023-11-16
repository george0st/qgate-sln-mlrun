"""
  UC401: Create feature vector(s)
"""

from qgate.uc.ucbase import UCBase
from qgate.solution import Solution
from qgate.uc.ucoutput import UCOutput


class UC401(UCBase):

    def __init__(self, sln: Solution, output: UCOutput):
        super().__init__(sln, output, self.__class__.__name__)


    @property
    def desc(self) -> str:
        return "Create feature vector(s)"

    def exec(self):
        self.sln.create_featurevector(self)

