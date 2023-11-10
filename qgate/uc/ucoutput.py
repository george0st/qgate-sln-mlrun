import datetime
import os, platform, sys
import mlrun
from qgate.uc.ucsetup import UCSetup

class Singleton (type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class UCOutput(metaclass=Singleton):
    """
    Management reports/outputs from use cases
    """

    COMMENT = "# "

    def __init__(self, setup: UCSetup):

        self._setup=setup
        if not os.path.exists(self._setup.model_output):
            os.makedirs(self._setup.model_output)
        self._file = open(os.path.join(self._setup.model_output, "qgate-sln-mlrun.txt"), 'w+t')

        self._headr()

    def __del__(self):
        self._file.close()

    def _headr(self):
        self._print(datetime.datetime.now().isoformat())
        self._print()

        self._print("MLRun:    " + mlrun.get_version() + " (https://docs.mlrun.org/en/latest/change-log/index.html)")
        self._print("Python:   " + sys.version)
        self._print("System:   " + platform.system() + " " + platform.version() + " (" + platform.platform() + ")")
        self._print("Platform: " + platform.machine()+ " (" + platform.processor() + ")")

        self._print()

        self._print("DIR = " + os.getcwd())
        self._print(str(self._setup).replace('\n',"\n" + UCOutput.COMMENT))


    def print(self, uc_name, *args, **kwargs):
        self._print(uc_name + str.format(args, kwargs), False)

    def _print(self, text=None, comment: bool=True):
        if comment:
            self._file.write(UCOutput.COMMENT)
        self._file.write((text if text else "") + '\n')


