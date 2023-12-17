from qgate.solution import Solution
from qgate.ts import ts101, ts102, ts201, ts301, ts401, ts501, ts601
from qgate.ts import tsbase
from qgate import output, setup
import sys


if __name__ == '__main__':

    setup = setup.Setup("0-size-100",
                          ["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"])
    output = output.Output(setup, ['./assets/templates/qgt-mlrun.txt',
                                   './assets/templates/qgt-mlrun.html'])
    sln = Solution(setup)

    testscenario_fns = [ts101.TS101, ts201.TS201, ts301.TS301, ts401.TS401, ts501.TS501]
    testscenario_test = ts601.TS601
    NoDelete=False

    # support parametr 'NoDelete' and 'Test' for switch-off the UC102: Delete project(s)
    if len(sys.argv)>1:
        for arg in sys.argv[1:]:
            arg=arg.lower()
            if arg=="nodelete":
                NoDelete=True
            elif arg=="test":
                testscenario_fns.append(testscenario_test)
    if not NoDelete:
        testscenario_fns.append(ts102.TS102)

    for testscenario_fn in testscenario_fns:
        if testscenario_fn:
            ts = testscenario_fn(sln, output)
        try:
            ts.exec()
            ts.state = tsbase.TSState.OK
        except Exception as ex:
            ts.state = tsbase.TSState.Error
            ts.testcase_detail(f"{type(ex).__name__}: {str(ex)}")
            ts.testcase_state("Error")
    output.render()
    output.close()