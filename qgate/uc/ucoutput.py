import datetime
import multiprocessing
import os, platform, sys
import mlrun
from qgate.uc.ucsetup import UCSetup
from contextlib import suppress
from qgate.version import __version__
from jinja2 import Template

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
    OUTPUT_FILE = "qg-mlrun-{0}.txt"
    JINJA_TEMPLATE = "./asset/qg-template.html"
    JINJA_OUTPUT_FILE = "qg-mlrun-{0}.html"

    def __init__(self, setup: UCSetup):

        self._setup=setup
        self._file_name=str.format(UCOutput.OUTPUT_FILE, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

        if not os.path.exists(self._setup.model_output):
            os.makedirs(self._setup.model_output)
        self._log_file = open(os.path.join(self._setup.model_output, self._file_name), 'w+t')
        self._headr()


    def _render(self):
        # https://zetcode.com/python/jinja/
        # https://ultraconfig.com.au/blog/jinja2-a-crash-course-for-beginners/
        data={}
        jinja=Template(UCOutput.JINJA_TEMPLATE)
        jinja.render(data)
        # TODO: save based on JINJA_OUTPUT_FILE

    @property
    def file_pattern(self):
        return UCOutput.OUTPUT_FILE
    @property
    def file_name(self):
        return self._file_name

    def __del__(self):
        self.Close()

    def Close(self):
        if self._log_file:
            self._footer()
            self._log_file.close()
            self._log_file=None


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

    def log(self, *args, **kwargs):
        self._log(str.format(*args, **kwargs), False)

    def logln(self, *args, **kwargs):
       self._logln(str.format(*args, **kwargs), False)

    def loghln(self, uc_name):
        self._log_file.write(uc_name + '\n')

    def _logln(self, text = None, comment: bool = True):
        if comment:
            self._log_file.write(UCOutput.COMMENT)
        self._log_file.write(text + '\n')

    def _log(self, text = None, comment: bool = True):
        if comment:
            self._log_file.write(UCOutput.COMMENT)
        if text:
            self._log_file.write(text)

