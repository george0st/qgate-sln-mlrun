"""
  UC501: Get data from off-line feature vector(s)
"""

from qgate.uc.ucbase import UCBase
from qgate.solution import Solution
from qgate.output import Output


class UC501(UCBase):

    def __init__(self, sln: Solution, output: Output):
        super().__init__(sln, output, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Get data from off-line feature vector(s)"

    @property
    def long_desc(self):
        return "Get data from off-line feature vector"

    def exec(self):
        self.sln.get_data_offline(self)

