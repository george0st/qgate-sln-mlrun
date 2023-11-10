
from qgate.uc.ucsetup import UCSetup
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

    def __init__(self, setup: UCSetup, name):
        self._setup=setup
        self._name=name

    @property
    def desc(self):
        raise NotImplemented()

    def _get_json_header(self, json_content):
        """ Get common header from config files

        :param json_content:    json content
        :return:                name, description, labels and kind from header
        """
        name = json_content['name']
        desc = json_content['description']
        kind = json_content['kind']

        # optional labels
        lbls = None if json_content.get('labels') is None else json_content.get('labels')
        return name, desc, lbls, kind

    @property
    def name(self):
        return self._name

    @staticmethod
    def str2bool(v):
        return v.lower() in ("yes", "true", "t", "1")

    @staticmethod
    def str2array(v):
        bulks = []
        for itm in v.split('|'):
            sub_itm = itm.split(',')
            if len(sub_itm)==2:
                bulk = [int(sub_itm[0]), int(sub_itm[1])]
            elif len(sub_itm)==3:
                bulk = [int(sub_itm[0]), int(sub_itm[1]), str(sub_itm[2]).strip()]
            else:
                bulk = []
            bulks.append(bulk)
        return bulks
