
from qgate.uc.ucoutput import UCOutput
import mlrun
import os

class UCSetup:
    """
    Shared setup as singleton for all use cases
    """

    def __init__(self, data_size, mlrun_env_file: list[str], output: UCOutput):

        self._output=output
        self._log(f"Mlrun version: {mlrun.get_version()}")

        # set variables based on environment files
        for env_file in mlrun_env_file:
            if os.path.isfile(env_file):
                self._variables=mlrun.set_env_from_file(env_file, return_dict=True)
                break

        # set model dir
        self._model_definition=self._variables['QGATE_DEFINITION']
        self._model_output=self._variables['QGATE_OUTPUT']

        # set projects
        self._projects=[]
        self._data_size=data_size
