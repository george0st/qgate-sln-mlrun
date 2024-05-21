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
        return "Simple pipeline(s), focus on full/partial event and tests under the Mock"

    def exec(self):
        """Simple pipeline during ingest"""
        self._class_plus(f"*/class_plus (event)", True)
        self._class_plus(f"*/class_plus", False)
        self._class_multipl(f"*/class_multipl (event)", True)
        self._class_multipl(f"*/class_multipl", False)
        self._minus(f"*/minus (event)", True)
        self._minus(f"*/minus", False)

    @TSBase.handler_testcase
    def _class_plus(self, testcase_name, full_event):

        func = mlrun.code_to_function(f"ts601_fn",
                                      kind="serving",
                                      filename="./qgate_sln_mlrun/ts/ts06_pipeline/ts601_ext_code.py")
        graph_echo = func.set_topology("flow")
        graph_echo.to(class_name="TS601Pipeline", full_event=full_event, name="plus", default=True).respond()

        # tests
        echo_server = func.to_mock_server(current_function="*")
        result = echo_server.test("", {"a": 5, "b": 7})
        echo_server.wait_for_completion()

        # value check
        if result['calc']!=12:
            raise ValueError("Invalid calculation, expected value 12")

    @TSBase.handler_testcase
    def _class_multipl(self, testcase_name, full_event):

        func = mlrun.code_to_function(f"ts601_fn",
                                      kind="serving",
                                      filename="./qgate_sln_mlrun/ts/ts06_pipeline/ts601_ext_code.py")
        graph_echo = func.set_topology("flow")
        graph_echo.to(class_name="TS601Pipeline", full_event=full_event, name="multipl", default=True).respond()

        # tests
        echo_server = func.to_mock_server(current_function="*")
        result = echo_server.test("", {"a": 5, "b": 7})
        echo_server.wait_for_completion()

        # value check
        if result['calc']!=35:
            raise ValueError("Invalid calculation, expected value 35")

    @TSBase.handler_testcase
    def _minus(self, testcase_name, full_event):
        func = mlrun.code_to_function(f"ts601_fn",
                                      kind="serving",
                                      filename="./qgate_sln_mlrun/ts/ts06_pipeline/ts601_ext_code.py")
        graph_echo = func.set_topology("flow")
        graph_echo.to(handler="minus" , full_event=full_event, name="minus", default=True).respond()

        # tests
        echo_server = func.to_mock_server(current_function="*")
        result = echo_server.test("", {"a": 10, "b": 7})
        echo_server.wait_for_completion()

        # value check
        if result['calc']!=3:
            raise ValueError("Invalid calculation, expected value 3")