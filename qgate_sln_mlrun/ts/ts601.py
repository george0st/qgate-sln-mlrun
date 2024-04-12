"""
  TS601: Simple pipeline for DataFrame source
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun.feature_store as fstore


class TS601(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Simple pipeline for DataFrame source"

    @property
    def long_desc(self):
        return "Simple pipeline for DataFrame source"

    def exec(self, project_name):
        pass

