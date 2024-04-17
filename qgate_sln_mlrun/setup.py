
import mlrun
import os
import json
from enum import Enum


class ProjectDelete(Enum):
    NO_DELETE = 0
    FULL_DELETE = 1
    PART_DELETE = 2

class Singleton (type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Setup(metaclass=Singleton):
    """
    Setup for solution
    """

    def __init__(self, mlrun_env_file: list[str], dataset_name = None, hard_variables: dict=None):
        """Define setting for testing

        :param mlrun_env_file:  list of *.env files, first valid file will be
                                used e.g. ["qgate-sln-mlrun-private.env", "qgate-sln-mlrun.env"]
        :param dataset_name:    name of data set e.g. "01-size-100"
        :param hard_variables:  new or replacement of variables from *.env file
        """
        # set variables based on environment files
        for env_file in mlrun_env_file:
            if os.path.isfile(env_file):
                self._variables=mlrun.set_env_from_file(env_file, return_dict=True)
                break

        # push dataset name
        if dataset_name:
            self._variables["QGATE_DATASET"] = dataset_name

        # create new or rewrite variables
        if hard_variables:
            for key in hard_variables.keys():
                self._variables[key]=hard_variables[key]

        self._variables["DIR"]=os.getcwd()

        # model definition setting
        self._model_definition_setting={}
        with open(os.path.join(self.model_definition, "01-model", "model.json"), "r") as json_file:
            setting = json.load(json_file)
        self._model_definition_setting=setting["spec"]

    def __str__(self):
        ret=""
        for key in self._variables.keys():
            ret+=key+ ": "+ "'" + str(self._variables[key]) + "'\n"
        return ret[:-1]

    @property
    def variables(self):
        variable_list=[]
        for key in self._variables.keys():
            itm = {}
            itm['key']=key
            itm['value']=self._variables[key]
            variable_list.append(itm)
        return variable_list

    @property
    def model_output(self):
        """Return the model output path"""
        return self._variables.get('QGATE_OUTPUT', './output')

    @property
    def model_definition(self):
        """Return the path to model definition"""
        return self._variables['QGATE_DEFINITION']

    @property
    def dataset_name(self):
        """Return the dataset setting"""
        return self._variables.get("QGATE_DATASET", "01-size-100")

    @property
    def filter_projects(self):
        """Return the project filter setting"""
        return self._variables.get("QGATE_FILTER_PROJECTS", None)

    @property
    def filter_scenarios(self):
        """Return the test scenario filter setting"""
        return self._variables.get("QGATE_FILTER_SCENARIOS", None)

    @property
    def redis(self):
        """Return the connection to Redis"""
        return self._variables.get('QGATE_REDIS', None)

    @property
    def mysql(self):
        """Return the connection to MySql"""
        return self._variables.get('QGATE_MYSQL', None)

    @property
    def postgres(self):
        """Return the connection to Postgres"""
        return self._variables.get('QGATE_POSTGRES', None)

    @property
    def kafka(self):
        """Return the connection to Kafka"""
        return self._variables.get('QGATE_KAFKA', None)

    @property
    def anonym_mode(self) -> bool:
        """Return the anonymous mode"""
        return True if self._variables.get('QGATE_ANONYM_MODE', "Off").lower() == "on" else False

    @property
    def csv_separator(self):
        return self._model_definition_setting["CSV_SEPARATOR"]

    @property
    def csv_decimal(self):
        return self._model_definition_setting["CSV_DECIMAL"]

    def get_scenario_setting(self, name):
        return self._variables.get(name, None)

    def set_scenario_setting(self, name, val):
        self._variables[name] = val

    @property
    def scenario(self):
        """Return the connection to Kafka"""
        return self._variables.get('QGATE_KAFKA', None)


