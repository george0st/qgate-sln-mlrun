"""
  TS602: Complex pipeline(s)
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
from qgate_sln_mlrun.setup import Setup
import mlrun.feature_store as fstore
import mlrun
import pandas as pd
import glob
import os


class TS602(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Complex pipeline(s)"

    @property
    def long_desc(self):
        return "Complex pipeline(s)"

    def exec(self):
        """Simple pipeline during ingest"""
        self._complex_pipeline(f"*/complex (event)")


    @TSBase.handler_testcase
    def _class_complex(self, testcase_name):

        func = mlrun.code_to_function(f"ts602_fn",
                                      kind="serving",
                                      filename="./qgate_sln_mlrun/ts/ts06_pipeline/ts602_ext_code.py")
        graph_echo = func.set_topology("flow")
        (graph_echo.to(class_name="TS602Pipeline", full_event=True, name="step1") \
                .to(class_name="TS602Pipeline", full_event=True, name="step2") \
                .to(class_name="TS602Pipeline", full_event=True, name="step3")
                .to(class_name="TS602Pipeline", full_event=True, name="step4").respond())

        # tests
        echo_server = func.to_mock_server(current_function="*")
        result = echo_server.test("", {"a": 5, "b": 7})
        echo_server.wait_for_completion()

    @TSBase.handler_testcase
    def _complex(self, testcase_name):

        func = mlrun.code_to_function(f"ts602_fn",
                                      kind="serving",
                                      filename="./qgate_sln_mlrun/ts/ts06_pipeline/ts602_ext_code.py")
        graph_echo = func.set_topology("flow")
        graph_echo.to(handler="second", full_event=True, name="step1") \
                .to(handler="second", full_event=True, name="step2") \
                .to(handler="third", full_event=True, name="step3") \
                .to(handler="third", full_event=True, name="step4").respond()

        # tests
        echo_server = func.to_mock_server(current_function="*")
        result = echo_server.test("", {"a": 5, "b": 7})
        echo_server.wait_for_completion()


