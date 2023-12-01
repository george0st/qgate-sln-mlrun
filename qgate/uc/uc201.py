"""
  UC201: Create feature set(s)
"""

from qgate.uc.ucbase import UCBase
from qgate.solution import Solution
from qgate.output import Output


class UC201(UCBase):

    def __init__(self, sln: Solution, output: Output):
        super().__init__(sln, output, self.__class__.__name__)


    @property
    def desc(self) -> str:
        return "Create feature set(s)"

    @property
    def long_desc(self):
        return "Create feature set with name, description, entities, features and targets"

    def exec(self):
        self.sln.create_featureset(self)

