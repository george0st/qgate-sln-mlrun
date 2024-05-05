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
        self._simple_pipeline_plus(f"{project_name}/simple_pipeline_plus", project_name)
        self._simple_pipeline_multipl(f"{project_name}/simple_pipeline_multipl", project_name)

    @TSBase.handler_testcase
    def _simple_pipeline_plus(self, testcase_name, project_name, featureset_name, file):

        func = mlrun.code_to_function(f"ts601_{project_name}_fn", kind="serving", filename="./ts601_ext_code.py")
        graph_echo = func.set_topology("flow")
        graph_echo.to(class_name="TS601Pipeline", full_event=True, name="plus", default=True).respond()

        # tests
        echo_server = func.to_mock_server(current_function="*")
        result = echo_server.test("", {"a": 5, "b": 7})
        echo_server.wait_for_completion()

        # value check
        if result['calc']!=12:
            raise Exception("Invalid calculation, expected value 12")

    @TSBase.handler_testcase
    def _simple_pipeline_multipl(self, testcase_name, project_name, featureset_name, file):

        func = mlrun.code_to_function(f"ts601_{project_name}_fn", kind="serving", filename="./ts601_ext_code.py")
        graph_echo = func.set_topology("flow")
        graph_echo.to(class_name="TS601Pipeline", full_event=True, name="multipl", default=True).respond()

        # tests
        echo_server = func.to_mock_server(current_function="*")
        result = echo_server.test("", {"a": 5, "b": 7})
        echo_server.wait_for_completion()

        # value check
        if result['calc']!=35:
            raise Exception("Invalid calculation, expected value 35")
