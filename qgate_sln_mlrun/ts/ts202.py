"""
  TS202: Create feature set(s) & Ingest from DataFrame source (in one step)
"""
import datetime
import sqlalchemy
from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore
from mlrun.features import Feature
from mlrun.data_types.data_types import ValueType
from mlrun.datastore.targets import RedisNoSqlTarget, ParquetTarget, CSVTarget, SQLTarget, KafkaTarget
import os
import json
import glob
import pandas as pd


class TS202(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Create feature set(s) & Ingest from DataFrame source (in one step)"

    @property
    def long_desc(self):
        return ("Create feature set(s) & Ingest from DataFrame source (in one step)")

    def exec(self, project_name):
        """ Get or create featuresets"""

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
                    self._create_featureset_ingest(f'{project_name}/{featureset_name}', project_name, json_file)

    @TSBase.handler_testcase
    def _create_featureset_ingest(self, testcase_name, project_name, json_file):
        json_content = json.load(json_file)
        name, desc, lbls, kind = TSBase.get_json_header(json_content)

        if kind == "feature-set":
            # create feature set only in case, if not exist
            featureset=self._create_featureset_content(project_name, name, desc, json_content['spec'])

            # TODO: get the relevant data file

            # ingest data with bundl/chunk
            for data_frm in pd.read_csv(file,
                                        sep=self.setup.csv_separator,
                                        header="infer",
                                        decimal=self.setup.csv_decimal,
                                        compression="gzip",
                                        encoding="utf-8",
                                        chunksize=10000):
                featureset.ingest(data_frm,
                              # overwrite=False,
                              return_df=False,
                              #infer_options=mlrun.data_types.data_types.InferOptions.Null)
                              infer_options=mlrun.data_types.data_types.InferOptions.default())
                # TODO: use InferOptions.Null with python 3.10 or focus on WSL
                # NOTE: option default, change types
                # NOTE: option Null, generate error with datetime in python 3.9



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

        for target in project_spec["targets"]:
            target = target.lower().strip()

            # add target
            if len(target) == 0:  # support bypass: switch empty targets
                continue
            target_provider = self._create_target(target, f"target_{count}", project_name, json_spec)
            if target_provider:
                target_providers.append(target_provider)
            count += 1
        fs.set_targets(target_providers, with_defaults=False)

        fs.save()
        return fs

    def _get_sqlschema(self, json_spec):
        schema = {}
        for item in json_spec['entities']:
            schema[item['name']] = TS201.type_to_type(item['type'])
        for item in json_spec['features']:
            schema[item['name']] = TS201.type_to_type(item['type'])
        return schema, json_spec['entities'][0]['name']

    def _create_target(self, target, target_name, project_name, json_spec):

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
                # mysql+<dialect>://<username>:<password>@<host>:<port>/<db_name>
                # mysql+pymysql://testuser:testpwd@localhost:3306/test

                tbl_name = f"{project_name}_{target_name}r"

                # TODO: create table as work-around, because create_table=True does not work for Postgres, only for MySQL
                #self._createtable(self.setup.mysql, tbl_name, json_spec)

                sql_schema, primary_key=self._get_sqlschema(json_spec)
                target_provider = SQLTarget(name=target_name, db_url=self.setup.mysql, table_name=tbl_name,
                                            schema=sql_schema,
                                            create_table=True,
                                            primary_key_column=primary_key)
            else:
                raise ValueError("Missing value for mysql connection, see 'QGATE_MYSQL'.")
        elif target == "postgres":
            if self.setup.postgres:
                # postgresql+<dialect>://<username>:<password>@<host>:<port>/<db_name>
                # postgresql+psycopg2://testuser:testpwd@localhost:5432/test

                tbl_name = f"{project_name}_{target_name}"

                # TODO: create table as work-around, because create_table=True does not work for Postgres, only for MySQL
                #self._createtable(self.setup.postgres, tbl_name, json_spec)

                sql_schema, primary_key=self._get_sqlschema(json_spec)
                target_provider = SQLTarget(name=target_name, db_url=self.setup.postgres, table_name=tbl_name,
                                            schema=sql_schema,
                                            create_table=True,
                                            primary_key_column=primary_key)
            else:
                raise ValueError("Missing value for mysql connection, see 'QGATE_POSTGRES'.")
        elif target == "kafka":
            if self.setup.kafka:
                params=self.setup.kafka.split(',')

                # NOTE: The path contains the Topic name
                target_provider = KafkaTarget(name=target_name, bootstrap_servers=params[0].strip(), path=params[1].strip())
            else:
                raise ValueError("Missing value for kafka connection, see 'QGATE_KAFKA'.")
        else:
            # TODO: Add support other targets
            raise NotImplementedError()
        return target_provider

    def _createtable(self, db_url, table_name, json_spec):
        # https://medium.com/@sandyjtech/creating-a-database-using-python-and-sqlalchemy-422b7ba39d7e

        engine = sqlalchemy.create_engine(db_url, echo=False)
        meta = sqlalchemy.MetaData()

        # create table definition
        tbl=sqlalchemy.Table(table_name, meta)
        # create primary keys
        for item in json_spec['entities']:
            tbl.append_column(
                sqlalchemy.Column( item['name'],TS201.type_to_sqlalchemy(item['type']), primary_key=True))
        # create columns
        for item in json_spec['features']:
            tbl.append_column(
                sqlalchemy.Column(item['name'], TS201.type_to_sqlalchemy(item['type'])))

        # create table
        meta.create_all(engine)

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
            "list": ValueType.STRING_LIST
        }
        if data_type not in type_map:
            raise TypeError(f"Unsupported type '{data_type}'")
        return type_map[data_type]

    @staticmethod
    def type_to_type(data_type):
        type_map = {
            "int": int,
            "int64": int,
            "uint64": int,
            "int128": int,
            "uint128": int,
            "float": float,
            "double": float,
            "boolean": bool,
            "bool": bool,
            "timestamp": datetime.datetime.timestamp,
            "datetime": datetime.datetime,
            "string": str,
            "list": list
        }
        if data_type not in type_map:
            raise TypeError(f"Unsupported type '{data_type}'")
        return type_map[data_type]

    @staticmethod
    def type_to_sqlalchemy(data_type):
        type_map = {
            "int": sqlalchemy.Integer,
            "int64": sqlalchemy.Integer,
            "uint64": sqlalchemy.Integer,
            "int128": sqlalchemy.BigInteger,
            "uint128": sqlalchemy.BigInteger,
            "float": sqlalchemy.Float,
            "double": sqlalchemy.Float,
            "boolean": sqlalchemy.Boolean,
            "bool": sqlalchemy.Boolean,
            "timestamp": sqlalchemy.TIMESTAMP,
            "datetime": sqlalchemy.DateTime,
            "string": sqlalchemy.String(50)
        }
        if data_type not in type_map:
            raise TypeError(f"Unsupported type '{data_type}'")
        return type_map[data_type]

