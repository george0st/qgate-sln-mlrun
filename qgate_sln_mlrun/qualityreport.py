import glob
import json
import os
from qgate_sln_mlrun.setup import Setup
from qgate_sln_mlrun.output import Output
from qgate_sln_mlrun.ts import ts101, ts102, ts201, ts301, ts401, ts501, ts502, ts601
from qgate_sln_mlrun.ts import tsbase


class QualityReport:
    """
    Quality report
    """

    TEST_SCENARIOS = [ts101.TS101, ts201.TS201, ts301.TS301, ts401.TS401, ts501.TS501, ts502.TS502]
    TEST_EXPERIMENTS = [ts601.TS601]
    TEST_SCENARIO_DELETE = ts102.TS102

    def __init__(self, setup: Setup, output: Output):
        self._setup = setup
        self._output = output

        self._projects = []
        self._project_specs = {}
        self._test_setting = {}

        self.load_test_setting()

    def build_scenarios_functions(self, delete_scenario=True, experiment_scenario=False) -> list[tsbase.TSBase]:
        test_scenario_functions = list(QualityReport.TEST_SCENARIOS)

        # add experiments
        if experiment_scenario:
            for experiment in QualityReport.TEST_EXPERIMENTS:
                test_scenario_functions.append(experiment)

        # add delete
        if delete_scenario:
            test_scenario_functions.append(QualityReport.TEST_SCENARIO_DELETE)

        return test_scenario_functions

    def execute(self, delete_scenario=True, experiment_scenario=False):

        test_scenario_functions = self.build_scenarios_functions(delete_scenario, experiment_scenario)

        for test_scenario_fn in test_scenario_functions:
            if test_scenario_fn:
                ts = test_scenario_fn(self)
                try:
                    # TODO: add standart logger
                    print(f"{ts.name}: {ts.desc} ...")
                    ts.exec()
                    ts.state = tsbase.TSState.DONE
                except Exception as ex:
                    ts.state = tsbase.TSState.ERR
                    ts.testcase_detail(f"{type(ex).__name__}: {str(ex)}")
                    ts.testcase_state("ERR")
        self._output.render()
        self._output.close()

    def load_test_setting(self):
        """Load setting for test execution from model\03-test\*-vector.json """

        source_file = os.path.join(os.getcwd(),
                                   self.setup.model_definition,
                                   "03-test",
                                   f"*-vector.json")

        # check existing data set
        for file in glob.glob(source_file):
            # iterate cross all featureset definitions
            with open(file, "r") as json_file:
                json_content = json.load(json_file)
                self._test_setting['vector'] = json_content["spec"]

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

    @property
    def test_setting(self) -> dict:
        return self._test_setting
