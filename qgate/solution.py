import mlrun
import mlrun.feature_store as fstore
from mlrun.features import Feature
from mlrun.data_types.data_types import spark_to_value_type
from mlrun.projects.project import MlrunProject
import json
import glob
import os


class Solution:
    """Create solution"""

    def __init__(self, mlrun_env_file: list[str]):
        """Create solution

        :param mlrun_env_file:  path to *.env files
        :param model_dir:       path do the 'qgate-fs-model'
        """

        # set variables
        for env_file in mlrun_env_file:
            if os.path.isfile(env_file):
                self._variables=mlrun.set_env_from_file(env_file, return_dict=True)
                break

        # set model dir
        self._model_dir=self._variables['QGATE-FS-MODEL']

        # set projects
        self._projects=[]

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
        targets=json_spec['targets']
        fs.set_targets(targets, with_defaults=False)

        fs.save()


    def _get_or_create_featuresets(self, project_name: str, project_spec: list[str], force: bool):
        """ Get or create featuresets

        :param project_name:    project name
        :param project_spec:    project specification
        :param force:           create in each case, default is True
        """
        dir=os.path.join(os.getcwd(), self._model_dir, "01-model", "02-feature-set", "*.json")
        for file in glob.glob(dir):

            # iterate cross all featureset definitions
            with open(file, "r") as json_file:
                json_content = json.load(json_file)
                name, desc, lbls, kind=self._get_json_header(json_content)

                if kind=="feature-set":
                    if name in project_spec:        # build only featuresets based on project spec
                        if force:
                            # create feature set, independent on exiting one
                            self._create_featureset(name, desc, json_content['spec'])
                            self._log(f"  Created featureset '{name}'")
                        else:
                            # create feature set only in case that it does not exist
                            try:
                                fstore.get_feature_set(f"{project_name}/{name}")
                                self._log(f"  Used featureset '{name}'")
                            except:
                                self._create_featureset(name, desc, json_content['spec'])
                                self._log(f"  Created featureset '{name}'")

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
        dir=os.path.join(os.getcwd(), self._model_dir, "01-model", "01-project", "*.json")
        for file in glob.glob(dir):
            with open(file, "r") as json_file:
                json_content = json.load(json_file)
                name, desc, lbls, kind=self._get_json_header(json_content)

                #TODO: asset kind

                # create project
                self._log(f"Creating project '{name}'")
                self._projects.append(name)
                prj=mlrun.get_or_create_project(name, context="./", user_project=False)
                prj.description=desc
                for lbl in lbls:
                    prj.metadata.labels[lbl]=lbls[lbl]
                prj.save()

                # create featureset
                self._get_or_create_featuresets(name, json_content['spec'], force)

                self._log(f"Created project '{name}'")


    def create(self, force: bool):
        """Create solution

        :param force:   create parts of solution in each case, default is True
        """

        # create projects
        self._get_or_create_projects(force)

    def delete(self):
        """Delete solution"""

        for prj_name in self._projects:
            mlrun.get_run_db().delete_project(prj_name, mlrun.api.schemas.constants.DeletionStrategy.cascade)
            self._log(f"!!! Deleted project '{prj_name}'")






