from qgate.setup import Setup


class ModelSolution:
    """Create solution"""

    def __init__(self, setup: Setup):
        """ Init

        :param setup:   Setup for the solution
        """
        self._setup=setup
        self._projects=[]
        self._project_specs={}

    @property
    def setup(self) -> Setup:
        return self._setup

