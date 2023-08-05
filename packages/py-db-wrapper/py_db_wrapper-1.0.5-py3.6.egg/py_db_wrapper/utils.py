import datetime
import pandas as pd
import logging
import os
import collections

class HiveUtils(object):

    class HiveSchema(object):
        def __init__(self,hive_engine, database, tablename, schema):
            self.database = database
            self.tablename = tablename
            self.schema = schema
            self.hive_engine = hive_engine

        def __str__(self):
            return '{} {} {}'.format(self.database, self.tablename, str(self.schema))

    @staticmethod
    def check_table_exists(hive_engine, database, tablename):
        query = "show tables in {db} like '{tb}'".format(db=database,tb=tablename)
        res = pd.read_sql(query, hive_engine)
        if len(res.index) > 0:
            return True
        else:
            return False

    @classmethod
    def describe_table(cls, hive_engine, database, tablename, return_type=pd.DataFrame):
        """
        Return a pd dataframe or dictinoary that describes the tables schema
        """
        if cls.check_table_exists(hive_engine, database, tablename):
            sql_string = 'describe {db}.{tb}'.format(db=database,tb=tablename)
            desc = pd.read_sql(sql_string, hive_engine)
            if return_type == pd.DataFrame:
                return desc
            elif return_type == HiveUtils.HiveSchema:
                hs = HiveUtils.HiveSchema(
                    hive_engine=hive_engine,
                    database=database, 
                    tablename=tablename, 
                    schema=dict(zip(desc['col_name'], desc['data_type']))
                    )
                return hs            


class RdbmsUtils(object):

    @staticmethod
    def read_table(connection, table_name):
        return pd.read_sql('select * from {}'.format(table_name),connection)

    @staticmethod
    def build_create_table_string(dialect, sql_schema, db_name, tablename):
        if dialect == 'mssql+pymssql':
            cols = ', '.join([' '.join([key, value]) for key, value in sql_schema.items()])
            sql_string = 'CREATE TABLE [{schema}].[{table}] ({cols})'.format(schema=db_name, table=tablename, cols=cols)
            logging.debug(sql_string)
            return sql_string
        elif dialect == 'postgresql':
            cols = ', '.join([' '.join([key, value]) for key, value in self.sql_schema.items()])
            sql_string = 'CREATE TABLE {table} ({cols})'.format(schema=db_name, table=tablename, cols=cols)
            logging.debug(sql_string)
            return sql_string
        else:
            logging.debug('No Dialect Defined')

    @classmethod
    def create_table_object(cls, sql_engine, dialect, sql_schema, db_name, tablename): 
        sql = cls.build_create_table_string(dialect, sql_schema, db_name, tablename)     
        sql_engine.execute(sql)

    
    @staticmethod
    def convert_schema(hive_schema, dialect):
        sql_schema = {}
        for col in hive_schema.schema:
            col_name = col
            split = hive_schema.schema[col].split('(')
            col_type = ''
            col_length = None
            if len(split) > 1:
                col_type = split[0].upper()
                if 'DECIMAL' in col_type:
                    col_length = None
                else:
                    col_length = int(split[1][:-1])
            else:
                col_type = hive_schema.schema[col].upper()
            #translate types
            new_type = None
            if 'CHAR' in col_type or 'STRING' in col_type:
                if dialect == 'mysql+pymysql':
                    new_type = 'VARCHAR({}) NULL DEFAULT NULL'.format(col_length)
                elif dialect == 'mssql+pymssql':
                    new_type = '[nvarchar](max) NULL'
                elif dialect == 'postgresql':
                    new_type = 'TEXT NULL DEFAULT NULL'
                else:
                    new_type = None
            elif 'LOB' in col_type:
                if dialect in ['mysql+pymysql', 'postgresql']:
                    new_type = 'TEXT NULL DEFAULT NULL'
                elif dialect == 'mssql+pymssql':
                    new_type = '[text] NULL'
                elif dialect == 'postgresql':
                    new_type = 'TEXT NULL DEFAULT NULL'
                else:
                    new_type = None
            elif 'NUM' in col_type or 'DOUBLE' in col_type or 'DECIMAL' in col_type:
                if dialect == 'mysql+pymysql':
                    new_type = 'NUMERIC NULL DEFAULT NULL'
                elif dialect == 'mssql+pymssql':
                    new_type = '[decimal](18, 2) NULL'
                elif dialect == 'postgresql':
                    new_type = 'NUMERIC NULL DEFAULT NULL'
                else:
                    new_type = None
            elif 'DATE' in col_type:
                if dialect == 'mysql+pymysql':
                    new_type = 'DATE NULL DEFAULT NULL'
                elif dialect == 'mssql+pymssql':
                    new_type = '[date] NULL'
                elif dialect == 'postgresql':
                    new_type = 'DATE NULL DEFAULT NULL'
                else:
                    new_type = None
            elif 'TIME' in col_type:
                if dialect == 'mysql+pymysql':
                    new_type = 'DATETIME(6) NULL DEFAULT NULL'
                elif dialect == 'mssql+pymssql':
                    new_type = '[datetime2](7) NULL'
                elif dialect == 'postgresql':
                    new_type = 'TIMESTAMP NULL DEFAULT NULL'
                else:
                    new_type = None
            elif col_type.upper() == 'INT':
                if dialect == 'mysql+pymysql':
                    new_type = 'INT NULL DEFAULT NULL'
                elif dialect == 'mssql+pymssql':
                    new_type = '[int] NULL'
                elif dialect == 'postgresql':
                    new_type = 'INT NULL DEFAULT NULL'
                else:
                    new_type = None
            elif col_type.upper() == 'BIGINT':
                if dialect == 'mysql+pymysql':
                    new_type = 'BIGINT NULL DEFAULT NULL'
                elif dialect == 'mssql+pymssql':
                    new_type = '[bigint] NULL'
                elif dialect == 'postgresql':
                    new_type = 'BIGINT NULL DEFAULT NULL'
                else:
                    new_type = None
            else:
                logging.debug(' '.join([col_name, col_type, "Column type not defined"]))
            if new_type:
                new_col = new_type
                if dialect == 'mysql+pymysql':
                    sql_schema.update({''.join(['`', col_name, '`']): new_col})
                elif dialect == 'mssql+pymssql':
                    sql_schema.update({''.join(['[', col_name, ']']): new_col})
                elif dialect == 'postgresql':
                    sql_schema.update({''.join(['"', col_name, '"']): new_col})
                else:
                    pass
            else:
                logging.debug(' '.join([col_name, col_type, "Column type not specified"]))
        return sql_schema


