import datetime
import multiprocessing
import os, platform, sys
import mlrun
from qgate.uc.ucsetup import UCSetup
from contextlib import suppress
from qgate.version import __version__

class Singleton (type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


#class UCOutput(metaclass=Singleton):
class UCOutput():

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
        self._footer()

    def __del__(self):
        self._footer()
        self._file.close()

    def _headr(self):
        self._logln("QGate version: " + __version__)
        self._logln(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def _footer(self):
        total, free = self._memory()
        self._logln("-----------------------")
        self._logln("Host: " + self._host())
        self._logln("RAM total/free: " + total + "/" + free)
        self._logln("CPU: " + str(multiprocessing.cpu_count()))
        self._logln("-----------------------")
        self._logln("MLRun: " + mlrun.get_version() + " (https://docs.mlrun.org/en/latest/change-log/index.html)")
        self._logln("Python: " + sys.version)
        self._logln("System: " + platform.system() + " " + platform.version() + " (" + platform.platform() + ")")
        self._logln("Platform: " + platform.machine() + " (" + platform.processor() + ")")
        self._logln("-----------------------")

        self._logln("DIR: '" + os.getcwd() + "'")
        self._logln(str(self._setup).replace('\n', "\n" + UCOutput.COMMENT))

    def _memory(self):

        mem_total, mem_free = "", ""
        with suppress(Exception):
            import psutil

            values = psutil.virtual_memory()
            mem_total = f"{round(values.total / (1073741824), 1)} GB"
            mem_free = f"{round(values.free / (1073741824), 1)} GB"
        return mem_total, mem_free

    def _host(self):
        """ Return information about the host in format (host_name/ip addr)"""

        host = ""
        with suppress(Exception):
            import socket

            host_name = socket.gethostname()
            ip = socket.gethostbyname(host_name)
            host = f"{host_name}/{ip}"
        return host

    def log(self, uc_name, *args, **kwargs):
        self._log(uc_name + str.format(*args, **kwargs), False)

    def logln(self, uc_name, *args, **kwargs):
        self._logln(uc_name + str.format(*args, **kwargs), False)

    def _logln(self, text = None, comment: bool = True):
        self._log((text if text else "") + '\n', comment)

    def _log(self, text = None, comment: bool = True):
        if comment:
            self._file.write(UCOutput.COMMENT)
        self._file.write((text if text else ""))

