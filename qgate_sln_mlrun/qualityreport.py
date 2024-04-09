import glob
import json
import os
from qgate_sln_mlrun.setup import Setup, ProjectDelete
from qgate_sln_mlrun.output import Output
from qgate_sln_mlrun.ts import ts101, ts102, ts201, ts301, ts302, ts303, ts401, ts501, ts502, ts701, ts801
from qgate_sln_mlrun.ts import tsbase
import logging
import importlib.resources


class QualityReport:
    """
    Quality report
    """

    TEST_SCENARIOS = [ts101.TS101,
                      ts201.TS201,
                      ts301.TS301, ts302.TS302, ts303.TS303,
                      ts401.TS401,
                      ts501.TS501, ts502.TS502]
    TEST_EXPERIMENTS = [ts701.TS701, ts801.TS801]
    TEST_SCENARIO_DELETE = ts102.TS102

    def __init__(self, setup: Setup, output: Output):
        self._setup = setup
        self._output = output

        self._projects = []
        self._project_descs = {}
        self._project_specs = {}
        self._test_setting = {}

        self.load_test_setting()

    def build_scenarios(self,
                        delete_scenario: ProjectDelete = ProjectDelete.FULL_DELETE,
                        experiment_scenario=False) -> list[tsbase.TSBase]:
        test_scenarios = list(QualityReport.TEST_SCENARIOS)

        # add experiments
        if experiment_scenario:
            for experiment in QualityReport.TEST_EXPERIMENTS:
                test_scenarios.append(experiment)

        # add delete
        if delete_scenario != ProjectDelete.NO_DELETE:
            test_scenarios.append(QualityReport.TEST_SCENARIO_DELETE)
            self.setup.set_scenario_setting("TS102_DELETE", delete_scenario)

        return test_scenarios

    def _define_testscenarios_based_projects(self):
        
        pass

    def execute(self, delete_scenario: ProjectDelete=ProjectDelete.FULL_DELETE, experiment_scenario=False, filter_projects: list=None):

        # define valid projects
        self._define_projects(filter_projects)

        # TODO: Define, which test scenarios will be valid for specific project
        self._define_testscenarios_based_projects()

        test_scenarios = self.build_scenarios(delete_scenario, experiment_scenario)

        logger = logging.getLogger("mlrun")
        for test_scenario in test_scenarios:
            if test_scenario:
                # create instance
                ts = test_scenario(self)
                try:
                    logger.info(f"!! Testing {ts.name}: {ts.desc} ...")
                    # prepare before execution of test case
                    ts.prepare()
                    # execution of test case
                    ts.exec()
                    ts.state = tsbase.TSState.DONE
                except Exception as ex:
                    ts.state = tsbase.TSState.ERR
                    ts.testcase_detail(f"{type(ex).__name__}: {str(ex)}")
                    ts.testcase_state("ERR")
        self._output.render(self.projects, self.project_descs)
        self._output.close()

    def _get_model_changes(self, resource):
        """
        Replacement of qgate_model content. It is useful for changes of default fehavioral
        (e.g. for different KafkaTarget handling, because KafkaTarget cannot work with FeatureVector, etc.).
        """
        package = "qgate_sln_mlrun.model_changes"

        try:
            with importlib.resources.open_text(package, resource) as input_file:
                return json.loads(input_file.read())
        except Exception as ex:
            pass
        return None

    def _define_projects(self, filter_projects: list=None):
        """
        Define valid projects based on QGATE_FILTER_PROJECTS, support project inheritance for 'spec'
        """
        dir=os.path.join(os.getcwd(), self.setup.model_definition, "01-model", "01-project", "**", "*.json")
        for file in glob.glob(dir, recursive=True):
            json_content=self._get_model_changes(os.path.basename(file))
            if json_content is None:
                with (open(file, "r") as json_file):
                    json_content = json.load(json_file)

            name, desc, lbls, kind, parent = tsbase.TSBase.get_json_header_full(json_content)

            # add project include project inheritance
            self._projects.append(name)
            self._project_descs[name] = [desc, lbls, kind, parent]
            self._project_specs[name] = json_content['spec']
            self._add_inheritance(name, parent)

        # cleanup filter_projects
        if filter_projects is None:
            if self.setup.filter_projects:
                filter_projects = [itm.strip() for itm in self.setup.filter_projects.split(',')]

        # apply filter, after inheritance
        if filter_projects:
            self._projects = [prj for prj in self._projects if prj in filter_projects]

    def _add_inheritance(self, project_name, parent):
        """Copy 'spec' content from parent project, but only for missing items"""
        if parent:
            for spec_item in self.project_specs[parent]:
                itm=self.project_specs[project_name].get(spec_item, None)
                if itm is None:
                    self.project_specs[project_name][spec_item]=self.project_specs[parent][spec_item]

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
    def project_descs(self) -> dict:
        return self._project_descs

    @property
    def project_specs(self) -> dict:
        return self._project_specs

    @property
    def test_setting(self) -> dict:
        return self._test_setting
