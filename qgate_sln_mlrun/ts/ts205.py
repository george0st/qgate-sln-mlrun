"""
  TS205: Create feature set(s) & Ingest from SQL source (one step)
"""
from qgate_sln_mlrun.ts.tsbase import TSBase
import mlrun
import mlrun.feature_store as fstore
from mlrun.data_types.data_types import ValueType
from mlrun.datastore.sources import SQLSource
from qgate_sln_mlrun.ts import ts201
import os
import json
import glob
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
import sqlalchemy
import pymysql.cursors

class TS205(TSBase):

    def __init__(self, solution):
        super().__init__(solution, self.__class__.__name__)

    @property
    def desc(self) -> str:
        return "Create feature set(s) & Ingest from SQL source (one step)"

    @property
    def long_desc(self):
        return ("Create feature set(s) & Ingest from SQL (MySQL) source (one step, without save and load featureset)")

    def create_table(self,featureset_name):
        primary_keys=""
        columns=""
        # Create source in MySQL for testing
        source_file = os.path.join(os.getcwd(),
                                   self.setup.model_definition,
                                   "01-model",
                                   "02-feature-set",
                                   f"*-{featureset_name}.json")

        for file in glob.glob(source_file):
            # iterate cross all featureset definitions
            with open(file, "r") as json_file:
                json_content = json.load(json_file)
                name, desc, lbls, kind = TSBase.get_json_header(json_content)

                # create SQL source based on the featureset
                json_spec=json_content['spec']

                # define entities
                for item in json_spec['entities']:
                    columns+=f"{item['name']} {TS205.type_to_mysql_type(item['type'])},"
                    primary_keys+=f"{item['name']},"

                # define features
                for item in json_spec['features']:
                    columns+=f"{item['name']} {TS205.type_to_mysql_type(item['type'])},"

        create_cmd=f"CREATE TABLE src_{featureset_name} ({columns[:-1]}, PRIMARY KEY ({primary_keys[:-1]}));"

        # Connect to the database
        connection = pymysql.connect(host='localhost:3306',
                                     user='testuser',
                                     password='testpwd',
                                     database='test',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                # create table
                cursor.execute(create_cmd)
                connection.commit()

                # insert data



        # command via SQLAlchemy
        # from sqlalchemy.sql import text
        # with engine.connect() as con:
        #
        #     data = ({"id": 1, "title": "The Hobbit", "primary_author": "Tolkien"},
        #             {"id": 2, "title": "The Silmarillion", "primary_author": "Tolkien"},
        #             )
        #
        #     statement = text("""INSERT INTO book(id, title, primary_author) VALUES(:id, :title, :primary_author)""")
        #
        #     for line in data:
        #         con.execute(statement, **line)

        # from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
        # conn = "mysql+pymysql://testuser:testpwd@localhost:3306/test"
        # engine = create_engine(conn, echo=True)
        # meta = MetaData()
        #
        # students = Table(
        #     'students', meta,
        #     Column('id', Integer, primary_key=True),
        #     Column('name', String),
        #     Column('lastname', String),
        # )
        # meta.create_all(engine)

    def exec(self, project_name):
        """ Create featuresets & ingest"""
        for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
            self.create_table(featureset_name)

        # TODO: test, if mySQL is available
        pass
        # for featureset_name in self.get_featuresets(self.project_specs.get(project_name)):
        #     # create file with definition of vector
        #     source_file = os.path.join(os.getcwd(),
        #                                self.setup.model_definition,
        #                                "01-model",
        #                                "02-feature-set",
        #                                f"*-{featureset_name}.json")
        #
        #     for file in glob.glob(source_file):
        #         # iterate cross all featureset definitions
        #         with open(file, "r") as json_file:
        #             self._create_featureset_ingest(f'{project_name}/{featureset_name}', project_name, json_file)

    @TSBase.handler_testcase
    def _create_featureset_ingest(self, testcase_name, project_name, json_file):
        json_content = json.load(json_file)
        name, desc, lbls, kind = TSBase.get_json_header(json_content)

        if kind == "feature-set":

            # create feature set based on the logic in TS201
            ts=ts201.TS201(self._solution)
            featureset=ts.create_featureset_content(project_name, f"{self.name}-{name}", desc, json_content['spec'])

            source_file = os.path.join(os.getcwd(),
                                       self.setup.model_definition,
                                       "02-data",
                                       self.setup.dataset_name,
                                       f"*-{name}.parquet")
            for file in glob.glob(source_file):

                fstore.ingest(featureset,
                              SQLSource(name="tst", path=file),
                              # overwrite=False,
                              return_df=False,
                              # infer_options=mlrun.data_types.data_types.InferOptions.Null)
                              infer_options=mlrun.data_types.data_types.InferOptions.default())
                # TODO: use InferOptions.Null with python 3.10 or focus on WSL
                # NOTE: option default, change types
                # NOTE: option Null, generate error with datetime in python 3.9

    def type_to_alchemy_type(data_type):
        type_map = {
            "int": sqlalchemy.Integer,
            "int64": sqlalchemy.BigInteger,
            "uint64": sqlalchemy.BigInteger,
            "int128": sqlalchemy.BigInteger,
            "uint128": sqlalchemy.BigInteger,
            "float": sqlalchemy.Float,
            "double": sqlalchemy.Float,
            "boolean": sqlalchemy.Boolean,
            "bool": sqlalchemy.Boolean,
            "timestamp": sqlalchemy.TIMESTAMP,
            "datetime": sqlalchemy.DateTime,
            "string": sqlalchemy.String
        }
        if data_type not in type_map:
            raise TypeError(f"Unsupported type '{data_type}'")
        return type_map[data_type]

    def type_to_mysql_type(data_type):
        type_map = {
            "int": "INT",
            "int64": "INT",
            "uint64": "INT",
            "int128": "INT",
            "uint128": "INT",
            "float": "float",
            "double": "float",
            "boolean": "bit",
            "bool": "bit",
            "timestamp": "timestamp",
            "datetime": "datetime",
            "string": "varchar(512)"
        }
        if data_type not in type_map:
            raise TypeError(f"Unsupported type '{data_type}'")
        return type_map[data_type]
