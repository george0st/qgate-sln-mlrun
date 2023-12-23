from qgate_sln_mlrun.qualityreport import QualityReport
from qgate_sln_mlrun import output, setup


if __name__ == '__main__':
    stp = setup.Setup("0-size-100",
                           ["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"])
    out = output.Output(stp, ['./qgate_sln_mlrun/templates/qgt-mlrun.txt',
                                   './qgate_sln_mlrun/templates/qgt-mlrun.html'])
    report=QualityReport(stp,out)

    # NoDelete = False
    #
    # # support parametr 'NoDelete' and 'Test' for switch-off the UC102: Delete project(s)
    # if len(sys.argv) > 1:
    #     for arg in sys.argv[1:]:
    #         arg = arg.lower()
    #         if arg == "nodelete":
    #             NoDelete = True
    #         elif arg == "test":
    #             testscenario_fns.append(testscenario_test)
    # if not NoDelete:
    #     testscenario_fns.append(ts102.TS102)

    report.execute()
