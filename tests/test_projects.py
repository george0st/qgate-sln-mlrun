from qgate_sln_mlrun.qualityreport import QualityReport
from qgate_sln_mlrun import output, setup
from qgate_sln_mlrun.setup import ProjectDelete
import unittest
import os


class TestProjects(unittest.TestCase):

    INPUT_FILE = "qgate-sln-mlrun.env"

    @classmethod
    def setUpClass(cls):
        # setup relevant path
        if not os.path.isfile(os.path.join(".", TestProjects.INPUT_FILE)):
            os.chdir(os.path.dirname(os.getcwd()))

    @classmethod
    def tearDownClass(cls):
        pass

    def test_template_file(self):
        # test based on external template files
        stp = setup.Setup(["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"],
                          None,
                          {"QGATE_OUTPUT": "./tests_output/"})
        out = output.Output(stp, ['./qgate_sln_mlrun/templates/qgt-mlrun.txt',
                                  './qgate_sln_mlrun/templates/qgt-mlrun.html'])
        report = QualityReport(stp, out)
        report.execute(ProjectDelete.PART_DELETE, True)

    def test_template_embeded(self):
        # test based on embeddit templates
        stp = setup.Setup(["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"],
                          None,
                          {"QGATE_OUTPUT": "./tests_output/"})
        out = output.Output(stp, [output.Output.DEFAULT_TEMPLATE_HTML, output.Output.DEFAULT_TEMPLATE_TXT])
        report = QualityReport(stp, out)
        report.execute(ProjectDelete.PART_DELETE, True)
