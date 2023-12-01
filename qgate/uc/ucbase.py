
from qgate.uc.output_template import OutputTemplate
#from qgate.solution import Solution
from enum import Enum


class UCState(Enum):
    NoExecution = 1
    OK = 2
    Error = 3

class UCBase:
    """
    Base class for all use cases
    """

    def __init__(self, sln, output: OutputTemplate, name: str):
        self._sln=sln
        self._output=output
        self._name=name
        self._state = UCState.NoExecution

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

    def log(self, *args, **kwargs):
        self.output.log(*args, **kwargs)

    def logln(self, *args, **kwargs):
        self.output.logln(*args, **kwargs)

    def loghln(self):
        self.output.loghln(self.name + ": " + self.desc)

