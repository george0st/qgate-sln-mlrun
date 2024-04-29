import pymysql.cursors
import os
import glob
import json
import pandas as pd
from qgate_sln_mlrun.ts.tsbase import TSBase
from qgate_sln_mlrun.ts.tshelper import TSHelper
from qgate_sln_mlrun.setup import Setup


class MySQLHelper():

    TABLE_SOURCE_PREFIX = "tmp_"

    def __init__(self,setup: Setup):
        self._setup = setup

    @property
    def setup(self) -> Setup:
        return self._setup

    @property
    def configured(self):
        """Return None if not configured or connection string (based on setting QGATE_MYSQL in *.env file"""
        return self.setup.mysql

    def create_table(self, featureset_name):
        """Create table in MySQL"""
        primary_keys=""
        column_types= ""
        columns = ""

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

                # primary keys
                for item in json_spec['entities']:
                    columns += f"{item['name']},"
                    column_types += f"{item['name']} {TSHelper.type_to_mysql_type(item['type'])},"
                    primary_keys += f"{item['name']},"

                # columns
                for item in json_spec['features']:
                    columns += f"{item['name']},"
                    column_types+= f"{item['name']} {TSHelper.type_to_mysql_type(item['type'])},"

        table_name = self._convert_feature_tablename(featureset_name)
        column_types = column_types[:-1].replace('-', '_')
        primary_keys = primary_keys[:-1].replace('-','_')
        columns = columns[:-1].replace('-', '_')

        # connect
        user_name, password, host, port, db = TSHelper.split_sqlalchemy_connection(self.setup.mysql)
        connection = pymysql.connect(host=host,
                                     port=port,
                                     user=user_name,
                                     password=password,
                                     database=db,
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:

                # drop table
                cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
                connection.commit()

                # create table
                #cursor.execute(f"CREATE TABLE {table_name} ({columns}, PRIMARY KEY ({primary_keys}));")
                cursor.execute(f"CREATE TABLE {table_name} ({column_types});")
                connection.commit()

                # insert data
                self._insert_into(connection, cursor, table_name, featureset_name, columns)

    def _insert_into(self, connection, cursor, table_name, featureset_name, columns):
        """Insert data into table in MySQL"""

        # create possible file for load
        source_file = os.path.join(os.getcwd(),
                                   self.setup.model_definition,
                                   "02-data",
                                   self.setup.dataset_name,
                                   f"*-{featureset_name}.csv.gz")

        for file in glob.glob(source_file):
            # ingest data with bundl/chunk
            for data_frm in pd.read_csv(file,
                                        sep=self.setup.csv_separator,  # ";",
                                        header="infer",
                                        decimal=self.setup.csv_decimal,  # ",",
                                        compression="gzip",
                                        encoding="utf-8",
                                        chunksize=10000):
                for row in data_frm.to_numpy().tolist():
                    values=f"\",\"".join(str(e) for e in row)

                    cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES(\"{values}\");")
                connection.commit()

    def _convert_feature_tablename(self, featureset_name):
        """Convert featureset name to the name of table.

        :param featureset_name:     feature set name
        :return:                    name of db table with relevant prefix
        """
        return f"{MySQLHelper.TABLE_SOURCE_PREFIX}{featureset_name}".replace('-', '_')

    def table_exist(self, featureset_name):
        """Check, if table in MySQL exist

        :param table_name:      name of the table for check
        :return:                True - table exist, False - table does not exist
        """
        user_name, password, host, port, db = TSHelper.split_sqlalchemy_connection(self.setup.mysql)
        connection = pymysql.connect(host=host,
                                     port=port,
                                     user=user_name,
                                     password=password,
                                     database=db,
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = {db}"
                               f" AND table_name = {self._convert_feature_tablename(featureset_name)} LIMIT 1;")
                myresult = cursor.fetchone()
                if myresult:
                    if len(myresult)>0:
                        return True
        return False
