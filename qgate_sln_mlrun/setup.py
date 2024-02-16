
import mlrun
import os

class Setup:
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

    def __str__(self):
        ret=""
        for key in self._variables.keys():
            ret+=key+ ": "+ "'" + self._variables[key] + "'\n"
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
        return self._variables.get('QGATE_OUTPUT', './output')

    @property
    def model_definition(self):
        return self._variables['QGATE_DEFINITION']

    @property
    def dataset_name(self):
        return self._variables.get("QGATE_DATASET", "01-size-100")

    @property
    def filter_projects(self):
        """Return project filter setting"""
        return self._variables.get("QGATE_FILTER_PROJECTS", None)

    @property
    def redis(self):
        """Return REDIS setting"""
        return self._variables.get('QGATE_REDIS', None)

    @property
    def mysql(self):
        """Return MYSQL setting"""
        return self._variables.get('QGATE_MYSQL', None)
