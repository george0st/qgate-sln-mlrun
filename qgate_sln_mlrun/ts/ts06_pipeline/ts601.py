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
        self._class_plus(f"{project_name}/pipeline_class_plus", project_name)
        self._class_multipl(f"{project_name}/pipeline_class_multipl", project_name)
        self._minus(f"{project_name}/pipeline_minus", project_name)

    @TSBase.handler_testcase
    def _class_plus(self, testcase_name, project_name):

        func = mlrun.code_to_function(f"ts601_{project_name}_plus",
                                      kind="serving",
                                      filename="./qgate_sln_mlrun/ts/ts06_pipeline/ts601_ext_code.py")
        graph_echo = func.set_topology("flow")
        graph_echo.to(class_name="TS601Pipeline", full_event=True, name="plus", default=True).respond()

        # tests
        echo_server = func.to_mock_server(current_function="*")
        result = echo_server.test("", {"a": 5, "b": 7})
        echo_server.wait_for_completion()

        # value check
        if result['calc']!=12:
            raise ValueError("Invalid calculation, expected value 12")

    @TSBase.handler_testcase
    def _class_multipl(self, testcase_name, project_name):

        func = mlrun.code_to_function(f"ts601_{project_name}_multipl",
                                      kind="serving",
                                      filename="./qgate_sln_mlrun/ts/ts06_pipeline/ts601_ext_code.py")
        graph_echo = func.set_topology("flow")
        graph_echo.to(class_name="TS601Pipeline", full_event=True, name="multipl", default=True).respond()

        # tests
        echo_server = func.to_mock_server(current_function="*")
        result = echo_server.test("", {"a": 5, "b": 7})
        echo_server.wait_for_completion()

        # value check
        if result['calc']!=35:
            raise ValueError("Invalid calculation, expected value 35")

    @TSBase.handler_testcase
    def _minus(self, testcase_name, project_name):
        func = mlrun.code_to_function(f"ts601_{project_name}_minus",
                                      kind="serving",
                                      filename="./qgate_sln_mlrun/ts/ts06_pipeline/ts601_ext_code.py")
        graph_echo = func.set_topology("flow")
        graph_echo.to(handler="minus" , full_event=True, name="minus", default=True).respond()

        # tests
        echo_server = func.to_mock_server(current_function="*")
        result = echo_server.test("", {"a": 10, "b": 7})
        echo_server.wait_for_completion()

        # value check
        if result['calc']!=3:
            raise ValueError("Invalid calculation, expected value 3")