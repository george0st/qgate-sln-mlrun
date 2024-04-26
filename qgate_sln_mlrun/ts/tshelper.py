import sqlalchemy
from mlrun.data_types.data_types import ValueType
import datetime
import re


class TSHelper:


    @staticmethod
    def split_sqlalchemy_connection(connection_string):
        """Parsing pattern 'mysql+<dialect>://<username>:<password>@<host>:<port>/<db_name>'

        :param connection_string:   connection string for parsing
        :return:                    None value or collection of items user name, password, host, port and db name
        """
        user_name = host = db = None
        password=""
        port=0

        if connection_string:
            # re.findall(r'\/\/(.*):(.*)@(.*):(.*)/(.*)', connection_string)
            configs = re.findall(r'//(.*):(.*)@(.*):(.*)/(.*)', connection_string)
            if configs and len(configs)>0:
                config=configs[0]
                if len(config)>=5:
                    user_name = config[0]
                    password = config[1]
                    host = config[2]
                    port = int(config[3]) if config[3] else 0
                    db = config[4]
        return user_name, password, host, port, db


    @staticmethod
    def type_to_mlrun_type(data_type) -> ValueType:
        """Mapping types from Quality Gate to MLRun types"""
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
        """Mapping types from Quality Gate to Python types"""
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
        """Mapping types from Quality Gate to SqlAlchemy types"""
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

    @staticmethod
    def type_to_mysql_type(data_type):
        """Mapping types from Quality Gate to MySQL types"""
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
            "string": "nvarchar(512)"
        }
        if data_type not in type_map:
            raise TypeError(f"Unsupported type '{data_type}'")
        return type_map[data_type]
