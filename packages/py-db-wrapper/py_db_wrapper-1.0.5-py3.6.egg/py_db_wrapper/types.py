from .exceptions import TYPE_NOT_DEFINED
from .dialects import *

class SQL_TYPE(object):
    """
    """

    TYPES = {}

    @classmethod
    def get_type_string(cls, dialect):
        return cls.TYPES[dialect]

class BIGINT(SQL_TYPE):
    """
    """
    TYPES = {
        Mssql: 'bigint',
        Mysql: 'BIGINT',
    }

class TINYINT(SQL_TYPE):
    """
    """
    TYPES = {
        Mssql: 'tinyint',
        Mysql: 'TINYINT'
    } 

TYPE_REGISTER = [
    BIGINT,
    TINYINT
    ]

def get_base_type_from_string(dialect, type_string):
    for type in TYPE_REGISTER:
        if type_string == type.TYPES[dialect]:
            return type
    raise TYPE_NOT_DEFINED

def convert_type_string(type_string, from_d, to_d):
    base_type = get_base_type_from_string(from_d, type_string)
    return base_type.get_type_string(to_d)

