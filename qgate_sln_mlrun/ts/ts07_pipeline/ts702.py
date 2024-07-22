"""
  TS702: Complex pipeline(s)
"""
from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun


class TS702(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Complex pipeline(s)"

    @property
    def long_desc(self):
        return "Complex pipeline(s) without relation to featureset/data ingest"

    def exec(self):
        """Simple pipeline during ingest"""
        self._class_complex(f"*/class_complex (event)")
        self._complex(f"*/complex (event)")


    @TSBase.handler_testcase
    def _class_complex(self, testcase_name):

        func = mlrun.code_to_function(f"ts702_fn",
                                      kind="serving",
                                      filename="./qgate_sln_mlrun/ts/ts07_pipeline/ts702_ext_code.py")
        graph_echo = func.set_topology("flow")
        graph_echo.to(class_name="TS702Pipeline", full_event=True, name="step1") \
                .to(class_name="TS702Pipeline", full_event=True, name="step2") \
                .to(class_name="TS702Pipeline", full_event=True, name="step3") \
                .to(class_name="TS702Pipeline", full_event=True, name="step4").respond()

        # tests
        echo_server = func.to_mock_server(current_function="*")
        result = echo_server.test("", {"a": 5, "b": 7})
        echo_server.wait_for_completion()

        # value check
        if result['calc']!=78177:
            raise ValueError("Invalid calculation, expected value 78177")

    @TSBase.handler_testcase
    def _complex(self, testcase_name):

        func = mlrun.code_to_function(f"ts702_fn",
                                      kind="serving",
                                      filename="./qgate_sln_mlrun/ts/ts07_pipeline/ts702_ext_code.py")
        graph_echo = func.set_topology("flow")
        graph_echo.to(handler="step1", full_event=True, name="step1") \
                .to(handler="step2", full_event=True, name="step2") \
                .to(handler="step3", full_event=True, name="step3") \
                .to(handler="step4", full_event=True, name="step4").respond()

        # tests
        echo_server = func.to_mock_server(current_function="*")
        result = echo_server.test("", {"a": 5, "b": 7})
        echo_server.wait_for_completion()

        # value check
        if result['calc']!=78177:
            raise ValueError("Invalid calculation, expected value 78177")


