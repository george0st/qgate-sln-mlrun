import mlrun
import mlrun.feature_store as fstore
from mlrun.features import Feature
from mlrun.data_types.data_types import spark_to_value_type
from mlrun.datastore import ParquetTarget
from mlrun.projects.project import MlrunProject
import json
import glob
import os
import pandas as pd


class Solution:
    """Create solution"""

    def __init__(self, data_size, mlrun_env_file: list[str]):
        """Create solution

        :param mlrun_env_file:  path to *.env files
        :param model_dir:       path do the 'qgate-fs-model'
        """

        # logging MLRun version
        self._log(f"Mlrun version: {mlrun.get_version()}")

        # set variables
        for env_file in mlrun_env_file:
            if os.path.isfile(env_file):
                self._variables=mlrun.set_env_from_file(env_file, return_dict=True)
                break

        # set model dir
        self._model_definition=self._variables['QGATE_DEFINITION']
        self._model_output=self._variables['QGATE_OUTPUT']

        # set projects
        self._projects=[]
        self._data_size=data_size

    def _create_featureset(self, featureset_name, featureset_desc, json_spec):
        """
        Create featureset based on json spec

        :param featureset_name:    feature name
        :param featureset_desc:    feature description
        :param json_spec:  Json specification for this featureset
        """

        fs = fstore.FeatureSet(
            name=featureset_name,
            description=featureset_desc
        )

        # define entities
        for item in json_spec['entities']:
            fs.add_entity(
                name=item['name'],
                value_type=spark_to_value_type(item['type']),
                description=item['description']
            )

        # define features
        for item in json_spec['features']:
            fs.add_feature(
                name=item['name'],
                feature=Feature(
                    value_type=spark_to_value_type(item['type']),
                    description=item['description']
                )
            )

        # define targets
        count=0
        target_providers=[]
        for target in json_spec['targets']:
            if target.lower().strip()=="parquet":
                # support more parquet targets
                target_name=f"target_{count}"
                target_providers.append(ParquetTarget(name=target_name, path=os.path.join(self._model_output,target_name)))
            else:
                # TODO: Add support other targets for MLRun CE e.g. RedisTarget
                raise NotImplementedError()
            count+=1
        fs.set_targets(target_providers, with_defaults=False)

        fs.save()
        return fs

    def _get_or_create_featuresets(self, project_name: str, project_spec: list[str], force: bool):
        """ Get or create featuresets

        :param project_name:    project name
        :param project_spec:    project specification
        :param force:           create in each case, default is True
        """
        dir=os.path.join(os.getcwd(), self._model_definition, "01-model", "02-feature-set", "*.json")
        for file in glob.glob(dir):

            # iterate cross all featureset definitions
            with open(file, "r") as json_file:
                json_content = json.load(json_file)
                name, desc, lbls, kind=self._get_json_header(json_content)

                if kind=="feature-set":
                    if name in project_spec:        # build only featuresets based on project spec
                        if force:
                            # create feature set, independent on exiting one
                            fs=self._create_featureset(name, desc, json_content['spec'])
                            self._log(f"  Created featureset '{name}'...")
                        else:
                            # create feature set only in case that it does not exist
                            try:
                                fs=fstore.get_feature_set(f"{project_name}/{name}")
                                self._log(f"  Used featureset '{name}'...")
                            except:
                                fs=self._create_featureset(name, desc, json_content['spec'])
                                self._log(f"  Created featureset '{name}'...")

                        # load data for specific featureset
                        self._load_data(name, fs)



    def _get_json_header(self, json_content):
        """ Get common header

        :param json_content: jsou content
        :return: name, description, labeles and kind from header
        """
        name = json_content['name']
        desc = json_content['description']
        kind = json_content['kind']

        # optional labels
        lbls = None if json_content.get('labels') is None else json_content.get('labels')
        return name, desc, lbls, kind

    def _log(self, info):
        """ Logging

        :param info: message
        """
        #        context=mlrun.get_or_create_ctx("gate")
        #        context.logger.info(info)
        print(info)

    def _get_or_create_projects(self, force: bool):
        # create projects
        dir=os.path.join(os.getcwd(), self._model_definition, "01-model", "01-project", "*.json")
        for file in glob.glob(dir):
            with open(file, "r") as json_file:
                json_content = json.load(json_file)
                name, desc, lbls, kind=self._get_json_header(json_content)

                #TODO: asset kind

                # create project
                self._log(f"Creating project '{name}'...")
                self._projects.append(name)
                prj=mlrun.get_or_create_project(name, context="./", user_project=False)
                prj.description=desc
                for lbl in lbls:
                    prj.metadata.labels[lbl]=lbls[lbl]
                prj.save()

                # create featureset
                self._get_or_create_featuresets(name, json_content['spec'], force)

    def create(self, force: bool):
        """Create solution

        :param force:   create parts of solution in each case, default is True
        """

        # create projects
        self._get_or_create_projects(force)


    def delete(self):
        """Delete solution"""

        self._log(f"Deleted ALL")
        for prj_name in self._projects:
            mlrun.get_run_db().delete_project(prj_name,"cascade")
            self._log(f"  Deleted project '{prj_name}' !!!")

        # TODO: clean output directory (self._model_output)

    def _load_data(self, featureset_name: str, featureset: mlrun.feature_store.feature_set):

        dir=os.path.join(os.getcwd(), self._model_definition, "02-data", self._data_size, f"*-{featureset_name}.csv.gz")
        for file in glob.glob(dir):
            self._log("    Load data...")

            for data_frm in pd.read_csv(file,
                                     sep=";",
                                     header="infer",
                                     decimal=",",
                                     compression="gzip",
                                     encoding="utf-8",
                                     chunksize=10000):
                fstore.ingest(featureset,
                              data_frm,
                              overwrite=False,
                              return_df=False,
                              infer_options=mlrun.data_types.data_types.InferOptions.Null)










