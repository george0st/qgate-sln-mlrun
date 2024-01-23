from qgate_sln_mlrun.qualityreport import QualityReport
from qgate_sln_mlrun import output, setup
import sys


if __name__ == '__main__':
    stp = setup.Setup(["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"])
    out = output.Output(stp, ['./qgate_sln_mlrun/templates/qgt-mlrun.txt',
                                   './qgate_sln_mlrun/templates/qgt-mlrun.html'])
    report=QualityReport(stp,out)

    delete_scenario = True
    test_scenario = False

    # support parametr 'NoDelete' and 'Test' for switch-off the UC102: Delete project(s)
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            arg = arg.lower()
            if arg == "nodelete":
                delete_scenario = False
            elif arg == "test":
                test_scenario=True

    report.execute(delete_scenario, test_scenario)
