import mlrun
import mlrun.feature_store as fstore
from mlrun.features import Feature
from mlrun.data_types.data_types import spark_to_value_type
import json
import os, glob


class Project:
    """Create project tttttt"""

    def __init__(self, envFile: str):
        """Create project

        :param envFile: path to *.env
        """
        self.envFile=envFile
        self.projects=[]


    def __createFeatureSet(self, jsonContent):
        """
        Create feature set based on json content
        :param jsonContent:  Json content
        :return:
        """

        fs = fstore.FeatureSet(
            name=jsonContent['name'],
            description=jsonContent['description']
        )

        # define entities
        for item in jsonContent['entities']:
            fs.add_entity(
                name=item['name'],
                value_type=spark_to_value_type(item['value_type']),
                description=item['description']
            )

        # define features
        for item in jsonContent['features']:
            fs.add_feature(
                name=item['name'],
                feature=Feature(
                    value_type=spark_to_value_type(item['value_type']),
                    description=item['description']
                )
            )

        # define targets
        try:
            targets = jsonContent['targets'].split(',')
        except:
            targets = ['parquet']
        fs.set_targets(targets, with_defaults=False)
        fs.save()

    def __get_or_createFeatureSet(self, projectName: str, jsonFile: str, force: bool):
        """
        Get or create feature set based on json definition file e.g. 'gate-01-basic-party.json'
        :param projectName:     Project name
        :param jsonFile:  Json definition file e.g. 'gate-01-basic-party.json'
        """
        with open(jsonFile, "r") as file:
            jsonContent = json.load(file)

            if force:
                # create feature set, independent on exiting one
                self.__createFeatureSet(jsonContent)
            else:
                # create feature set only in case that it does not exist
                try:
                    fstore.get_feature_set(f"{projectName}/{jsonContent['name']}")
                except:
                    self.__createFeatureSet(jsonContent)

    def createProject(self, projectName: str,force: bool):
        mlrun.set_env_from_file(self.envFile)

        self.projects.append(projectName)

        # create project
        project = mlrun.get_or_create_project(projectName, context="./", user_project=False)

        # create feature sets based on /assets/{projectName}*.json templates
        with mlrun.get_or_create_ctx(projectName) as context:
            for file in glob.glob(os.path.join(os.getcwd(),"assets",f"{projectName}*.json")):
                context.logger.info(f"Start, create feature set '{os.path.basename(file)}'")
                self.__get_or_createFeatureSet(projectName, file, force)
                context.logger.info(f"End, created feature set '{os.path.basename(file)}'")

    def delete(self):
        for prj in self.projects:
            print(f"> Delete '{prj}'")
            mlrun.get_run_db().delete_project(prj, mlrun.api.schemas.constants.DeletionStrategy.cascade)





