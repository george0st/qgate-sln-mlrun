"""
  TS601: Simple pipeline(s)
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
from qgate_sln_mlrun.setup import Setup
import mlrun.feature_store as fstore
import mlrun
import pandas as pd
import glob
import os


class TS601(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Simple pipeline(s)"

    @property
    def long_desc(self):
        return "Simple pipeline(s) and test with Mock"

    def exec(self, project_name):
        """Simple pipeline during ingest"""

        self.project_switch(project_name)

        self._ingest_data(f"{project_name}/*", project_name)

    @TSBase.handler_testcase
    def _simple_pipeline(self, testcase_name, project_name, featureset_name, file):

        func = mlrun.code_to_function("ts601_function", kind="serving", filename="./ts601_ext_code.py")
        graph_echo = func.set_topology("flow")
        graph_echo.to(class_name="TS601Pipeline", name="STEP1", default=True)

        # tests
        echo_server = func.to_mock_server(current_function="*")
        result = echo_server.test("", {"a": 100, "b": 200})
        echo_server.wait_for_completion()
        print(result)
