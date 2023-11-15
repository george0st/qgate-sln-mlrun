"""
  UC201: Create feature set(s)
"""

from qgate.uc.ucbase import UCBase
from qgate.nsolution import NSolution
from qgate.uc.ucoutput import UCOutput


class UC201(UCBase):

    def __init__(self, sln: NSolution, output: UCOutput):
        super().__init__(sln, output, self.__class__.__name__)


    @property
    def desc(self) -> str:
        return "Create feature set(s)"

    def exec(self):
        self.sln.create_featureset(self)

