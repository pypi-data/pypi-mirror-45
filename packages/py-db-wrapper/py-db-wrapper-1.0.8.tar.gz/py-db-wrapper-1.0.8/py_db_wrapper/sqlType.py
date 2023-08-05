from .exceptions import TYPE_NOT_DEFINED
from .dialect import *

class SqlType(object):
    """
    """

    TYPES = {}
    def __init__(self, size=None):
        self.size = size

    @classmethod
    def get_type_string(cls, dialect):
        return cls.TYPES[dialect]

    def type_specific_string_action(self, dialect):
        pass

    def sql_string(self, dialect):
        self.type_specific_string_action(dialect)
        if self.size:
            return '{}({})'.format(self.TYPES[dialect][0], self.size)
        else:
            return self.TYPES[dialect][0]
            

class BIGINT(SqlType):
    """
    """
    TYPES = {
        Mssql: ['bigint'],
        Mysql: ['BIGINT'],
        Hive: ['BIGINT']
    }

class TINYINT(SqlType):
    """
    """
    TYPES = {
        Mssql: ['tinyint'],
        Mysql: ['TINYINT'],
        Hive: ['TINYINT']
    } 

class INTEGER(SqlType):
    """
    """
    TYPES = {
        Mssql: ['int'],
        Mysql: ['INT'],
        Hive: ['INT', 'INTEGER']
    }

class DECIMAL(SqlType):
    """
    """
    TYPES = {
        Mssql: ['decimal', 'numeric'],
        Mysql: ['DECIMAL', 'NUMERIC'],
        Hive: ['DECIMAL', 'NUMERIC']
    }  

class DOUBLE(SqlType):
    """
    """
    TYPES = {
        Mssql: ['float'],
        Mysql: ['DOUBLE'],
        Hive: ['DOUBLE', 'DOUBLE PRECISION']
    }       

class DATE(SqlType):
    """
    """
    TYPES = {
        Mssql: ['date'],
        Mysql: ['DATE'],
        Hive: ['DATE']
    }  

class DATETIME(SqlType):
    """
    """
    TYPES = {
        Mssql: ['datetime2'],
        Mysql: ['DATETIME'],
        Hive: ['TIMESTAMP']
    }  

class TIMESTAMP(SqlType):
    """
    """
    TYPES = {
        Mssql: ['datetime2'],
        Mysql: ['TIMESTAMP'],
        Hive: ['TIMESTAMP']
    } 

class STRING(SqlType):
    """
    """
    TYPES = {
        Mssql: ['varchar'],
        Mysql: ['VARCHAR'],
        Hive: ['STRING', 'VARCHAR', 'CHAR', ]
    }  

    def type_specific_string_action(self, dialect):
        if 'CHAR' in self.TYPES[dialect][0].upper() and not self.size:
            self.size = 'max'

class BOOLEAN(SqlType):
    """
    """
    TYPES = {
        Mssql: ['bit'],
        Mysql: ['BOOLEAN'],
        Hive: ['BOOLEAN']
    }        

TYPE_REGISTER = [
    BIGINT,
    TINYINT,
    INTEGER,
    STRING,
    DECIMAL,
    DOUBLE,
    DATE,
    DATETIME,
    TIMESTAMP,
    BOOLEAN
    ]

def get_base_type_from_string(dialect, type_string):
    for sql_type in TYPE_REGISTER:
        if type_string.upper() in [x.upper() for x in sql_type.TYPES[dialect]]:
            return sql_type
    raise TYPE_NOT_DEFINED({'type_string':type_string, 'dialect':dialect})

def convert_type_string(type_string, from_d, to_d):
    base_type = get_base_type_from_string(from_d, type_string)
    return base_type.get_type_string(to_d)[0]

