"""
  TS501: Get data from on-line feature vector(s)
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore


class TS502(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Get data from on-line feature vector(s)"

    @property
    def long_desc(self):
        return "Get data from on-line feature vector"

    def exec(self):
        self.get_data_online()

    def get_data_online(self):
        pass

