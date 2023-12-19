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
        self._data={}
        self._templates=templates
        self._system_info()

# region TEST SCENARIOS
    def testscenario_new(self, ts_name, ts_description):
        new_ts = {}
        new_ts['name'] = ts_name
        new_ts['desc'] = ts_description
        new_ts['testcases']=[]
        if self._data.get("testscenarios"):
            self._data["testscenarios"].append(new_ts)
        else:
            self._data["testscenarios"]=[]
            self._data["testscenarios"].append(new_ts)

    def testcase_new(self, name):
        testcase={}
        testcase['name']=name
        testcase['detail']=None
        testcase['state']=None

        ts=self._data["testscenarios"][-1]
        ts['testcases'].append(testcase)

    def testcase_detail(self, detail):
        ts=self._data["testscenarios"][-1]
        if len(ts['testcases'])==0:
            self.testcase_new("GLOBAL")
        testcase = ts['testcases'][-1]
        testcase['detail']=detail

    def testcase_detailext(self, detail):
        ts = self._data["testscenarios"][-1]
        testcase = ts['testcases'][-1]
        testcase['detail'] = f"{testcase['detail']} {detail}"

    def testcase_state(self, state="DONE"):
        ts=self._data["testscenarios"][-1]
        testcase=ts['testcases'][-1]
        testcase['state']=state

# endregion

    def render(self):
        # https://zetcode.com/python/jinja/
        # https://ultraconfig.com.au/blog/jinja2-a-crash-course-for-beginners/
        # https://www.analyticsvidhya.com/blog/2022/04/the-ultimate-guide-to-master-jinja-template/

        self._summary()
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

    def _summary(self):
        self._data["summary"]={}
        count_testcases=0
        count_testcases_done=0
        first_errors= ""
        error_count=0

        self._data["summary"]["count_testscenarios"]=len(self._data["testscenarios"])
        for testscenario in self._data["testscenarios"]:
            for testcase in testscenario["testcases"]:
                if testcase['state']=="DONE":
                    count_testcases_done += 1
                else:
                    if error_count < 3:
                        error_count+=1
                        if first_errors != "":
                            first_errors= first_errors + "<br><br>"
                        first_errors= first_errors + f"#{error_count} ERR<br>{testscenario['name']}: {testscenario['desc']}<br>{testcase['name']}<br>{testcase['detail']}"
            count_testcases+=len(testscenario["testcases"])

        self._data["summary"]["state"]="DONE" if count_testcases==count_testcases_done else "ERR"
        self._data["summary"]["count_testcases"]=count_testcases
        self._data["summary"]["count_testcases_done"]=count_testcases_done
        self._data["summary"]["count_testcases_err"]=count_testcases-count_testcases_done
        self._data["summary"]["first_errors"]=first_errors


    def _system_info(self):
        self._data["version"] = __version__

        # import mlrun
        # run_db_factory = mlrun.db.factory.RunDBFactory()
        # print(run_db_factory)

        self._data["datetime"] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self._data["memory_total"], self._data["memory_free"] = self._memory()
        self._data["host"] = self._host()
        self._data["cpu"] = str(multiprocessing.cpu_count())
        self._data["mlrun"] = mlrun.get_version()
        self._data["mlrun_server"] = self._mlrun_server()
        self._data["python"] = sys.version

        self._data["system"] = platform.system() + " " + platform.version() + " (" + platform.platform() + ")"
        self._data["platform"] = platform.machine() + " (" + platform.processor() + ")"
        self._data["variables"] = self._setup.variables

    def _mlrun_server(self):
        # Return server MLRun version

        server_version=""
        with suppress(Exception):
            run_db_factory = mlrun.db.factory.RunDBFactory()
            server_version = run_db_factory._run_db.server_version
        return server_version

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
