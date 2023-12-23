from qgate_sln_mlrun.qualityreport import QualityReport
from qgate_sln_mlrun import output, setup


if __name__ == '__main__':
    stp = setup.Setup("0-size-100",
                           ["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"])
    out = output.Output(stp, ['./qgate_sln_mlrun/templates/qgt-mlrun.txt',
                                   './qgate_sln_mlrun/templates/qgt-mlrun.html'])
    report=QualityReport(stp,out)
    report.execute()
