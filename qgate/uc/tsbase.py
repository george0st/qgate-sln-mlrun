
from qgate.output import Output
#from qgate.solution import Solution
from enum import Enum


class TSState(Enum):
    NoExecution = 1
    OK = 2
    Error = 3

class TSBase:
    """
    Base class for all test scenarios
    """

    def __init__(self, sln, output: Output, name: str):
        self._sln=sln
        self._output=output
        self._name=name
        self._state = TSState.NoExecution

    @property
    def sln(self):
        return self._sln

    @property
    def output(self):
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



