"""
  TS704: Complex pipeline(s) for ingest
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
from qgate_sln_mlrun.setup import Setup
import mlrun.feature_store as fstore
import mlrun
import pandas as pd
import glob
import os


class TS704(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Complex pipeline(s) for ingest"

    @property
    def long_desc(self):
        return "Complex pipeline(s) for ingest"

    def exec(self):
        return

    @TSBase.handler_testcase
    def _complex(self, testcase_name, class_call):
        return