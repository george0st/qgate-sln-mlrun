from qgate_sln_mlrun.qualityreport import QualityReport
from qgate_sln_mlrun import output, setup
import unittest
import os


class TestCommon(unittest.TestCase):
    INPUT_FILE = "qgate-sln-mlrun.env"

    @classmethod
    def setUpClass(cls):
        # setup relevant path
        if not os.path.isfile(os.path.join(".", TestCommon.INPUT_FILE)):
            os.chdir(os.path.dirname(os.getcwd()))

    @classmethod
    def tearDownClass(cls):
        pass

    def test_setup_str(self):
        # Test only the setup
        stp = setup.Setup(["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"])
        print(str(stp))

    def test_setup_str2(self):
        # Test only the setup
        stp = setup.Setup(["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"],
                          None,
                          {"QGATE_OUTPUT": "./tests_output/"})
        print(str(stp))

    def test_scenarios_name_desc(self):
        # Test only descriptions
        stp = setup.Setup(["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"])
        out = output.Output(stp, [output.Output.DEFAULT_TEMPLATE_HTML, output.Output.DEFAULT_TEMPLATE_TXT])
        report = QualityReport(stp, out)
        test_scenarios = report.build_scenarios(True, True)

        for test_scenario in test_scenarios:
            tst = test_scenario(self)
            print(f"{tst.name}: {tst.desc}: {tst.long_desc}")

