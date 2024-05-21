import glob
import json
import os
from qgate_sln_mlrun.setup import Setup, ProjectDelete
from qgate_sln_mlrun.output import Output
from qgate_sln_mlrun.ts.ts09_serve_model import ts801
from qgate_sln_mlrun.ts.ts08_build_model import ts701
from qgate_sln_mlrun.ts.ts07_pipeline import ts601, ts602, ts603, ts604
from qgate_sln_mlrun.ts.ts06_get_data import ts501, ts502
from qgate_sln_mlrun.ts.ts05_feature_vector import ts401
from qgate_sln_mlrun.ts.ts03_ingest_data import ts301, ts302, ts303, ts304, ts305
from qgate_sln_mlrun.ts.ts02_feature_set import ts201, ts202, ts203, ts204, ts205, ts206
from qgate_sln_mlrun.ts.ts01_project import ts101, ts102
from qgate_sln_mlrun.ts import tsbase
import importlib.resources


class QualityReport:
    """
    Quality report
    """

    TEST_SCENARIOS = [ts101.TS101,
                      ts201.TS201, ts202.TS202, ts203.TS203, ts204.TS204, ts205.TS205, ts206.TS206,
                      ts301.TS301, ts302.TS302, ts303.TS303, ts304.TS304, ts305.TS305,
                      ts401.TS801,
                      ts501.TS801, ts502.TS702,
                      ts601.TS801, ts602.TS702, ts603.TS703, ts604.TS704]
    TEST_EXPERIMENTS = [ts701.TS801, ts801.TS801]
    TEST_SCENARIO_DELETE = ts102.TS102


    # Target vs On/Off-line
    TARGET_ONLINE = ["kafka", "redis", "mysql", "postgres"]
    TARGET_OFFLINE = ["parquet", "csv"]

    # Target vs invalid tests
    TARGET_NOT_VALID_TEST = {"kafka": ["TS501", "TS502"]}

    # Test vs Only On/Off-line
    TEST_BOTH = ["TS101","TS102",
                 "TS201", "TS202", "TS203", "TS204", "TS205", "TS206",
                 "TS301", "TS302", "TS303", "TS304", "TS305",
                 "TS401",
                 "TS601", "TS602", "TS603", "TS604"]
    TEST_ONLY_OFFLINE = ["TS501","TS701","TS801"]
    TEST_ONLY_ONLINE = ["TS502"]


    def __init__(self, setup: Setup, output: Output):
        self._setup = setup
        self._output = output

        self._projects = []
        self._project_descs = {}
        self._project_specs = {}
        self._project_scenarios = {}
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

    def _project_avoid_testscenarios(self, project):
        # Define test scenarios, which will be jumped (without execution)

        all_avoid=set()
        online = offline = False

        # identification of targets (I am focusing on project level)
        # TODO: focus on featureset level also
        spec=self.project_specs[project]
        for target in spec["targets"]:
            if target in self.TARGET_ONLINE:
                online=True
            if target in self.TARGET_OFFLINE:
                offline=True

            # add avoid based on target
            avoid=self.TARGET_NOT_VALID_TEST.get(target, None)
            if avoid:
                for name in avoid:
                    all_avoid.add(name)

        # add avoid TS based on missing On/Off-line targets
        if not offline:
            for name in self.TEST_ONLY_OFFLINE:
                all_avoid.add(name)
        if not online:
            for name in self.TEST_ONLY_ONLINE:
                all_avoid.add(name)
        return all_avoid

    def _projects_avoid_testscenarios(self):
        projects_avoid_ts={}
        for project_name in self.projects:
            projects_avoid_ts[project_name] = self._project_avoid_testscenarios(project_name)
        return projects_avoid_ts

    def execute(self, delete_scenario: ProjectDelete=ProjectDelete.FULL_DELETE, experiment_scenario=False, filter_projects: list=None):

        # define valid projects
        self._define_projects(filter_projects)

        # define, which test scenarios will be executed
        test_scenarios = self.build_scenarios(delete_scenario, experiment_scenario)

        # define, which test scenarios will be valid for specific project based on target type, etc.
        projects_avoid_ts = self._projects_avoid_testscenarios()

        # setup filter test scenarios
        filter_scenarios = [itm.strip() for itm in self.setup.filter_scenarios.split(',')] if self.setup.filter_scenarios else None

        for test_scenario in test_scenarios:
            if test_scenario:
                # create instance
                ts = test_scenario(self)
                try:

                    # apply QGATE_FILTER_SCENARIOS, focus on only the specific test scenarios
                    if filter_scenarios:
                        if not ts.name in filter_scenarios:
                            continue

                    # write info about TS to the output
                    ts.testscenario_new()

                    # BEFORE execution of TS
                    ts.before()
                    # EXEC execute of TS
                    ts.exec()

                    for project_name in self.projects:
                        if ts.name in projects_avoid_ts[project_name]:
                            # avoid irrelevant scenarios for this project
                            continue

                        # PRJ_EXEC execute of TS for project
                        ts.prj_exec(project_name)

                    # AFTER execute of TS
                    ts.after()
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
        Define valid projects based on QGATE_FILTER_PROJECTS, support project inheritance for 'spec'.

        Support project replacement based on local specification of projects in the folder './qgate_sln_mlrun/model_changes'
        """
        dir=os.path.join(os.getcwd(), self.setup.model_definition, "01-model", "01-project", "**", "*.json")
        for file in glob.glob(dir, recursive=True):
            # check, if it is possible to replace project based on project in './qgate_sln_mlrun/model_changes'
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
