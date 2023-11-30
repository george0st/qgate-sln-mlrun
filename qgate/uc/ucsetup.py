
import mlrun
import os

class UCSetup:
    """
    Setup for solution
    """

    def __init__(self, data_size, mlrun_env_file: list[str]):
        # set variables based on environment files
        for env_file in mlrun_env_file:
            if os.path.isfile(env_file):
                self._variables=mlrun.set_env_from_file(env_file, return_dict=True)
                break

        self._variables["DIR"]=os.getcwd()

        # set model dirs
        self._model_definition=self._variables['QGATE_DEFINITION']
        self._model_output=self._variables['QGATE_OUTPUT']

        # set data set size
        self._data_size=data_size

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
        return self._model_output

    @property
    def model_definition(self):
        return self._model_definition

    @property
    def data_size(self):
        return self._data_size