import sqlalchemy
from mlrun.data_types.data_types import ValueType
import datetime


class TSHelper:



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

