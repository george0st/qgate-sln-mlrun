import os
from qgate_sln_mlrun.setup import Setup
from qgate_sln_mlrun.output import Output
#from qgate_sln_mlrun.modelsolution import ModelSolution
from qgate_sln_mlrun.ts import ts101, ts102, ts201, ts301, ts401, ts501, ts601
from qgate_sln_mlrun.ts import tsbase
import sys

class QualityReport:
    """
    Quality reportn
    """

    def __init__(self, setup: Setup, output: Output):
        self._setup=setup
        self._output=output

        self._projects=[]
        self._project_specs={}

    def execute(self):
#        sln = ModelSolution(self._setup)

        testscenario_fns = [ts101.TS101, ts201.TS201, ts301.TS301, ts401.TS401, ts501.TS501]
        testscenario_test = ts601.TS601
        NoDelete = False

        # support parametr 'NoDelete' and 'Test' for switch-off the UC102: Delete project(s)
        if len(sys.argv) > 1:
            for arg in sys.argv[1:]:
                arg = arg.lower()
                if arg == "nodelete":
                    NoDelete = True
                elif arg == "test":
                    testscenario_fns.append(testscenario_test)
        if not NoDelete:
            testscenario_fns.append(ts102.TS102)

        for testscenario_fn in testscenario_fns:
            if testscenario_fn:
                ts = testscenario_fn(self)
                try:
                    ts.exec()
                    ts.state = tsbase.TSState.DONE
                except Exception as ex:
                    ts.state = tsbase.TSState.ERR
                    ts.testcase_detail(f"{type(ex).__name__}: {str(ex)}")
                    ts.testcase_state("ERR")
        self._output.render()
        self._output.close()

    @property
    def setup(self) -> Setup:
        return self._setup

    @property
    def output(self) -> Output:
        return self._output

    @property
    def projects(self) -> list:
        return self._projects

    @property
    def project_specs(self) -> dict:
        return self._project_specs

