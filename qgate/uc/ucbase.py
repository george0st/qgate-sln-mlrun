
from qgate.uc.ucsetup import UCSetup
from qgate.solution import Solution
from dotenv import dotenv_values
import mlrun
import mlrun.feature_store as fstore
from mlrun.features import Feature
from mlrun.data_types.data_types import spark_to_value_type
from mlrun.datastore import ParquetTarget
import json
import glob
import os
import pandas as pd
import shutil


class UCBase:
    """
    Base class for all use cases
    """

    def __init__(self, sln: Solution, name):
        self._name=name
        self._sln=sln

    @property
    def sln(self):
        return self._sln

    @property
    def setup(self):
        return self._sln._setup

    @property
    def desc(self):
        raise NotImplemented()

    @property
    def name(self):
        return self._name

    def exec(self):
        raise NotImplemented()


