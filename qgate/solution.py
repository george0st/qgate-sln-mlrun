import mlrun
import mlrun.feature_store as fstore
from mlrun.features import Feature
from mlrun.data_types.data_types import spark_to_value_type
from mlrun.projects.project import MlrunProject
import json
import os, glob


class Solution:
    """Create solution"""

    def __init__(self, mlrun_env_file: str, model_dir: str=f"qgate-fs-model"):
        """Create project

        :param mlrun_env_file: path to *.env
        """
        self.mlrun_env_file=mlrun_env_file
        self.model_dir=model_dir
        self.projects=[]

    def _create_featureset(self, feature_name, feature_desc, json_spec):
        """
        Create feature set based on json spec
        :param json_spec:  Json content
        :return:
        """

        fs = fstore.FeatureSet(
            name=feature_name,
            description=feature_desc
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


    def _get_or_create_featureset(self, project_name: str, spec: list[str], force: bool):
        dir=os.path.join(os.getcwd(), "..", self.model_dir, "01-model", "02-feature-set", "*.json")
        for file in glob.glob(dir):

            # check only relevant items
            with open(file, "r") as json_file:
                json_content = json.load(json_file)
                name, desc, lbls, kind=self._get_json_header(json_content)

                if kind=="feature-set":
                    if name in spec:
                        if force:
                            # create feature set, independent on exiting one
                            self._create_featureset(name, desc, json_content['spec'])
                        else:
                            # create feature set only in case that it does not exist
                            try:
                                fstore.get_feature_set(f"{project_name}/{name}")
                            except:
                                self._create_featureset(name, desc, json_content['spec'])


    def _get_json_header(self, json_content):
        name = json_content['name']
        desc = json_content['description']
        kind = json_content['kind']

        # optional labels
        lbls = None if json_content.get('labels') is None else json_content.get('labels')
        return name, desc, lbls, kind

    def log(self, info):
        #        context=mlrun.get_or_create_ctx("gate")
        #        context.logger.info(info)
        print(info)

    def _get_or_create_project(self, force: bool):
        # create projects
        dir=os.path.join(os.getcwd(), "..", self.model_dir, "01-model", "01-project", "*.json")
        for file in glob.glob(dir):
            with open(file, "r") as json_file:
                json_content = json.load(json_file)
                name, desc, lbls, kind=self._get_json_header(json_content)

                #TODO: asset kind

                # create project
                self.log(f"Init, project '{name}'")
                self.projects.append(name)
                prj=mlrun.get_or_create_project(name, context="./", user_project=False)
                prj.description=desc
                for lbl in lbls:
                    prj.metadata.labels[lbl]=lbls[lbl]
                prj.save()

                # create featureset
                self._get_or_create_featureset(name, json_content['spec'], force)

                self.log(f"Created, project '{name}'")


    def create(self, force: bool):

        # setup environment
        mlrun.set_env_from_file(self.mlrun_env_file)

        # create projects
        self._get_or_create_project(force)

    def delete(self):
        for prj in self.projects:
            mlrun.get_run_db().delete_project(prj, mlrun.api.schemas.constants.DeletionStrategy.cascade)






