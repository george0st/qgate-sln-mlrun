"""
  TS201: Create feature set(s)
"""

from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun.feature_store as fstore
from mlrun.features import Feature
from mlrun.data_types.data_types import ValueType
from mlrun.datastore.targets import RedisNoSqlTarget, ParquetTarget, CSVTarget, SQLTarget
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
        return ("Create feature set with name, description, entities, features and targets. "
                "Supported targes are these off-line 'parquet', 'csv' and the on-line 'redis'.")

    def exec(self):
        self.create_featuresets()

    def create_featuresets(self):
        """ Get or create featuresets
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

        project_spec = self.project_specs.get(project_name, None)
        self.project_switch(project_name)
        fs = fstore.FeatureSet(
            name=featureset_name,
            description=featureset_desc
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
            # TODO: check if current target == project targets, if yes than secondary cycle
            target=target.lower().strip()

            # check, if target is not project target
            project_target = self.get_project_target(project_spec, target)
            if project_target:
                # add project targets
                for sub_target in project_target:
                    sub_target = sub_target.lower().strip()
                    target_provider=self._create_target(sub_target, f"target_{count}", project_name)
                    if target_provider:
                        target_providers.append(target_provider)
                    count+=1
            else:
                # add target
                target_provider = self._create_target(target, f"target_{count}", project_name)
                if target_provider:
                    target_providers.append(target_provider)
                count += 1
        fs.set_targets(target_providers, with_defaults=False)

        fs.save()
        return fs

    def _create_target(self, target, target_name, project_name):

        target_provider=None
        if target == "parquet":
            # support more parquet targets (each target has different path)
            target_provider = ParquetTarget(name=target_name,
                                          path=os.path.join(self.setup.model_output, project_name, target_name))
        elif target == "csv":
            # ERR: it is not possible to use os.path.join in CSVTarget because issue in MLRun
#            pth="/".join(self.setup.model_output, project_name, target_name, target_name + ".csv")
            target_provider = CSVTarget(name=target_name,
                                        path="/".join([self.setup.model_output, project_name, target_name,
                                                      target_name + ".csv"]))
        elif target == "redis":
            if self.setup.redis:
                target_provider = RedisNoSqlTarget(name=target_name, path=self.setup.redis)
            else:
                raise ValueError("Missing value for redis connection, see 'QGATE_REDIS'.")
        elif target == "mysql":
            if self.setup.mysql:
                # mysql+pymysql://<username>:<password>@<host>:<port>/<db_name>
                # mysql+pymysql://testuser:testpwd@localhost:3306/test
                target_provider = SQLTarget(name=target_name, db_url=self.setup.mysql, table_name="",   # add value
                                            schema=None,                    # add value
                                            create_table=True,
                                            primary_key_column=None)       # add value

                # feature_set.set_targets(targets=[SQLTarget(name="we2", db_url=conn, table_name='my_table',
                #                                            schema={'party-id': int, 'party-type': str},
                #                                            create_table=True,
                #                                            primary_key_column='party-id')],
                #                         with_defaults=False)

                pass
            else:
                raise ValueError("Missing value for redis connection, see 'QGATE_REDIS'.")
        else:
            # TODO: Add support other targets for MLRun CE
            raise NotImplementedError()
        return target_provider

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
