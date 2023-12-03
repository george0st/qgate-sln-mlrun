import datetime
import multiprocessing
import os, platform, sys
import mlrun
from qgate.setup import Setup
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
class Output():
    """
    Management reports/outputs based on templates.
    """

    COMMENT = "# "
    OUTPUT_FILE = "qg-mlrun-{0}.txt"

    def __init__(self, setup: Setup, templates: [str]=None):
        """
        Initial

        :param setup:       specific usecase
        :param templates:   list of templates for generation outputs
        """

        self._setup=setup
        # self._file_name=str.format(Output.OUTPUT_FILE, datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
        self._data={}
        self._templates=templates

        # if not os.path.exists(self._setup.model_output):
        #     os.makedirs(self._setup.model_output)
        # self._log_file = open(os.path.join(self._setup.model_output, self._file_name), 'w+t')
        self._system_info()

    def new_usecase(self, uc_name, uc_description):
        new_uc = {}
        new_uc['name'] = uc_name
        new_uc['desc'] = uc_description
        new_uc['details']=[]
        if self._data.get("usecases"):
            self._data["usecases"].append(new_uc)
        else:
            self._data["usecases"]=[]
            self._data["usecases"].append(new_uc)

    def usecase_detail(self, detail):
        dtl={}
        dtl['detail']=detail
        dtl['state']=None

        uc=self._data["usecases"][-1]
        uc['details'].append(dtl)

    def usecase_detailext(self, detail):
        uc = self._data["usecases"][-1]
        dtl = uc['details'][-1]
        dtl['detail'] = f"{dtl['detail']} {detail}"

    def usecase_state(self, state="DONE"):
        uc=self._data["usecases"][-1]
        dtl=uc['details'][-1]
        dtl['state']=state

    def render(self):
        # https://zetcode.com/python/jinja/
        # https://ultraconfig.com.au/blog/jinja2-a-crash-course-for-beginners/
        # https://www.analyticsvidhya.com/blog/2022/04/the-ultimate-guide-to-master-jinja-template/
        for template in self._templates:

            # get template
            with open(os.path.join(template), 'r+t') as input_file:
                template_content=input_file.read()

            # render
            jinja=Template(template_content)
            output=jinja.render(data=self._data)

            # prepare output file
            path=os.path.split(template)
            file_name=path[-1:]
            extension=os.path.splitext(file_name[0])
            file_name=str.format("{0}-{1}{2}",extension[0],str.replace(self._data["datetime"],':','-'),
                                 extension[1])
            if not os.path.exists(self._setup.model_output):
                os.makedirs(self._setup.model_output)

            # write output
            with open(os.path.join(self._setup.model_output, file_name), 'w+t') as output_file:
                output_file.write(output)

    @property
    def file_pattern(self):
        return Output.OUTPUT_FILE
    @property
    def file_name(self):
        return self._file_name

    def __del__(self):
        self.close()

    def close(self):
        if self._data:
            del self._data
            self._data = None

    def _system_info(self):
        self._data["version"] = __version__
        self._data["datetime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self._data["memory_total"], self._data["memory_free"] = self._memory()
        self._data["host"] = self._host()
        self._data["cpu"] = str(multiprocessing.cpu_count())
        self._data["mlrun"] = mlrun.get_version()
        self._data["python"] = sys.version
        self._data["system"] = platform.system() + " " + platform.version() + " (" + platform.platform() + ")"
        self._data["platform"] = platform.machine() + " (" + platform.processor() + ")"
        self._data["variables"] = self._setup.variables


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
