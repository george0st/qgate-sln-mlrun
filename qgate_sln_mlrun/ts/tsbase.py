
from qgate_sln_mlrun.output import Output
#from qgate_sln_mlrun.modelsolution import ModelSolution
from qgate_sln_mlrun.qualityreport import QualityReport
from qgate_sln_mlrun.setup import Setup
from enum import Enum
import mlrun


class TSState(Enum):
    NoExecution = 1
    DONE = 2
    ERR = 3

class TSBase:
    """
    Base class for all test scenarios
    """

    def __init__(self, solution, output: Output, name: str):
        self._solution=solution
        self._setup=solution.setup
        self._output=output
        self._name=name
        self._state = TSState.NoExecution

    def handler_testcase(func):
        """Error handler for test case, mandatory arguments 'ts' and 'name'"""
        def wrapper(self, testcase_name: str, *args, **kwargs):

            try:
                self.testcase_new(testcase_name)
                ret=func(self, testcase_name, *args, **kwargs)
                self.testcase_state()
                return ret
            except Exception as ex:
                self.state = TSState.ERR
                self.testcase_detail(f"{type(ex).__name__}: {str(ex)}")
                self.testcase_state("ERR")
                return False
        return wrapper

# region INTERNAL

    # def has_featureset(self, name, project_spec):
    #     if project_spec:
    #         # Support two different collections
    #         if isinstance(project_spec, dict):
    #             return name in project_spec["feature-sets"]
    #         elif isinstance(project_spec, list):
    #             return name in project_spec
    #         else:
    #             raise Exception("Unsupported type")
    #     return False

    def get_featuresets(self, project_spec):
        if project_spec:
            # Support two different collections
            if isinstance(project_spec, dict):
                return project_spec["feature-sets"]
            elif isinstance(project_spec, list):
                return project_spec
            else:
                raise Exception("Unsupported type")
        return []

    def get_featurevectors(self, project_spec):
        # Support two different collections
        if isinstance(project_spec, dict):
            return project_spec["feature-vectors"]
        return []

    def get_json_header(self, json_content):
        """ Get common header

        :param json_content:    json content
        :return:                name, description, labeles and kind from header
        """
        name = json_content['name']
        desc = json_content['description']
        kind = json_content['kind']

        # optional labels
        lbls = None if json_content.get('labels') is None else json_content.get('labels')
        return name, desc, lbls, kind

# endregion

    @property
    def solution(self) -> QualityReport:
        return self._solution

    @property
    def setup(self) -> Setup:
        return self._setup

    @property
    def output(self) -> Output:
        return self._output

    @property
    def desc(self):
        raise NotImplemented()

    @property
    def long_desc(self):
        raise NotImplemented()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, a):
        self._state = a

    @property
    def name(self):
        return self._name

    def exec(self):
        raise NotImplemented()

    def project_switch(self, project_name):
        # switch to proper project if the current project is different
        if mlrun.get_current_project().name != project_name:
            mlrun.load_project(name=project_name, context="./", user_project=False)

    def testscenario_new(self):
        self.output.testscenario_new(self.name, self.desc)

    def testcase_new(self, name):
        self.output.testcase_new(name)

    def testcase_detail(self, detail):
        self.output.testcase_detail(detail)

    def testcase_detailext(self, detail):
        self.output.testcase_detailext(detail)

    def testcase_state(self, state="DONE"):
        self.output.testcase_state(state)



