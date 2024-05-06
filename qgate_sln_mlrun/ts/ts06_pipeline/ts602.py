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

    def exec(self, project_name):
        """Simple pipeline during ingest"""
        return
        # self.project_switch(project_name)
        # self._class_plus(f"{project_name}/class_plus (event)", project_name, True)
        # self._class_plus(f"{project_name}/class_plus", project_name, False)
        # self._class_multipl(f"{project_name}/class_multipl (event)", project_name, True)
        # self._class_multipl(f"{project_name}/class_multipl", project_name, False)
        # self._minus(f"{project_name}/minus (event)", project_name, True)
        # self._minus(f"{project_name}/minus", project_name, False)

    @TSBase.handler_testcase
    def _class_plus(self, testcase_name, project_name, full_event):

        func = mlrun.code_to_function(f"ts601_{project_name}_plus",
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

