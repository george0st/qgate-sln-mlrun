from qgate_sln_mlrun.modelsetup import ModelSetup


class ModelSolution:
    """Create solution"""

    def __init__(self, setup: ModelSetup):
        """ Init

        :param setup:   Setup for the solution
        """
        self._setup=setup
        self._projects=[]
        self._project_specs={}

    @property
    def setup(self) -> ModelSetup:
        return self._setup

    @property
    def projects(self) -> list:
        return self._projects

    @property
    def project_specs(self) -> dict:
        return self._project_specs
