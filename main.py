from qgate_sln_mlrun.qualityreport import QualityReport, ProjectDelete
from qgate_sln_mlrun import output, setup
import sys


if __name__ == '__main__':
    stp = setup.Setup(["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"])
    out = output.Output(stp, ['./qgate_sln_mlrun/templates/qgt-mlrun.txt',
                                   './qgate_sln_mlrun/templates/qgt-mlrun.html'])
    report=QualityReport(stp,out)

    delete_scenario = ProjectDelete.FULL_DELETE
    test_scenario = False

    # support parameters 'NoDelete' and 'Test' for switch-off the UC102: Delete project(s), ...
    if len(sys.argv) > 1:
        for arg in sys.argv[1:]:
            arg = arg.lower()
            if arg == "nodelete":
                delete_scenario = ProjectDelete.NO_DELETE
            if arg == "partdelete":
                delete_scenario = ProjectDelete.PART_DELETE
            elif arg == "test":
                test_scenario=True

    report.execute(delete_scenario, test_scenario)
