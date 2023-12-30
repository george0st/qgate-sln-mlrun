"""
  TS201: Create feature set(s)
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore
from mlrun.features import Feature
from mlrun.data_types.data_types import spark_to_value_type
from mlrun.data_types.data_types import ValueType
#from mlrun.datastore import ParquetTarget, CSVTarget
from mlrun.datastore.targets import RedisNoSqlTarget, ParquetTarget, CSVTarget
import os
import json
import glob


class TS201(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Create feature set(s)"

    @property
    def long_desc(self):
        return "Create feature set with name, description, entities, features and targets"

    def exec(self):
        self.create_featuresets()

    def create_featuresets(self):
        """ Get or create featuresets

        :param ts:      Test scenario
        """
        self.testscenario_new()
        for project_name in self.projects:
            for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
                # create file with definition of vector
                source_file = os.path.join(os.getcwd(),
                                           self.setup.model_definition,
                                           "01-model",
                                           "02-feature-set",
                                           f"*-{featureset_name}.json")

                for file in glob.glob(source_file):
                    # iterate cross all featureset definitions
                    with open(file, "r") as json_file:
                        self._create_featureset(f'{project_name}/{featureset_name}', project_name, json_file)

    @TSBase.handler_testcase
    def _create_featureset(self, testcase_name, project_name, json_file):
        json_content = json.load(json_file)
        name, desc, lbls, kind = TSBase.get_json_header(json_content)

        if kind == "feature-set":
            # create feature set only in case, if not exist
            try:
                fstore.get_feature_set(f"{project_name}/{name}")
            except:
                self._create_featureset_content(project_name, name, desc, json_content['spec'])

    def _create_featureset_content(self, project_name, featureset_name, featureset_desc, json_spec):
        """
        Create featureset based on json spec

        :param project_name:        project name
        :param featureset_name:     feature name
        :param featureset_desc:     feature description
        :param json_spec:  Json specification for this featureset
        """

        self.project_switch(project_name)
        fs = fstore.FeatureSet(
            name=featureset_name,
            description=featureset_desc,
            relations=json_spec.get('relations')
        )

        # define entities
        for item in json_spec['entities']:
            fs.add_entity(
                name=item['name'],
                value_type=TS201.type_to_mlrun_type(item['type']),
                description=item['description']
            )

        # define features
        for item in json_spec['features']:
            fs.add_feature(
                name=item['name'],
                feature=Feature(
                    value_type=TS201.type_to_mlrun_type(item['type']),
                    description=item['description']
                )
            )

        # define targets
        count=0
        target_providers=[]
        for target in json_spec['targets']:
            target_name = f"target_{count}"
            if target.lower().strip()=="parquet":
                # support more parquet targets (each target has different path)
                target_providers.append(ParquetTarget(name=target_name, path=os.path.join(self.setup.model_output, project_name, target_name)))
            elif target.lower().strip()=="csv":
                target_providers.append(CSVTarget(name=target_name, path=os.path.join(self.setup.model_output, project_name, target_name,target_name+".csv")))
            elif target.lower().strip()=="redis":
                if self.setup.redis:
                    target_providers.append(RedisNoSqlTarget(name=target_name, path=self.setup.redis))
                else:
                    raise ValueError("Invalid value for redis connection, see 'QGATE_REDIS'.")
            else:
                # TODO: Add support other targets for MLRun CE
                raise NotImplementedError()
            count+=1
        fs.set_targets(target_providers, with_defaults=False)

        fs.save()
        return fs

    @staticmethod
    def type_to_mlrun_type(data_type) -> ValueType:
        type_map = {
            "int": ValueType.INT64,
            "int64": ValueType.INT64,
            "uint64": ValueType.UINT64,
            "int128": ValueType.INT128,
            "uint128": ValueType.UINT128,
            "float": ValueType.FLOAT,
            "double": ValueType.DOUBLE,
            "boolean": ValueType.BOOL,
            "bool": ValueType.BOOL,
            "timestamp": ValueType.DATETIME,
            "datetime": ValueType.DATETIME,
            "string": ValueType.STRING,
            "list": ValueType.STRING_LIST,
        }
        if data_type not in type_map:
            raise TypeError(f"Unsupported type '{data_type}'")
        return type_map[data_type]
