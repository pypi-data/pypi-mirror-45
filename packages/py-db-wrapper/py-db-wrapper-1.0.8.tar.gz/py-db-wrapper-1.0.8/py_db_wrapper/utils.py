import datetime
import pandas as pd
import logging
import os
import collections
import re
import json
from py_db_wrapper import sqlType
from py_db_wrapper import dialect
from py_db_wrapper.exceptions import TABLE_NOT_FOUND
from py_db_wrapper.sql.statement import DescribeStatement, ShowTablesStatement


class HiveUtils(object):

    @staticmethod
    def check_table_exists(hive_engine, database, tablename):
        show_stmt = ShowTablesStatement(dialect.Hive)
        res = pd.read_sql(show_stmt.get_sql(schema=database), hive_engine)
        if tablename in res.iloc[ : , 0 ].tolist():
            return True
        else:
            return False


    @staticmethod
    def parse_describe_results(results):
        columns = []
        for result in results:
            name = result[0]
            
            sql_type_raw = result[1]
            sql_type_string = sql_type_raw.split('(')[0]
            search = re.search(r'\((.*?)\)',sql_type_raw)
            if search:
                sql_type_size = search.group(1)
            else:
                sql_type_size  =None
            sql_type = sqlType.get_base_type_from_string(dialect.Hive, sql_type_string)()
            sql_type.size = sql_type_size
            columns.append((name, sql_type))
        return columns
            

    @classmethod
    def get_table_columns(cls, hive_engine, database, tablename):
        """
        Return a pd dataframe or dictionary that describes the tables schema
        """
        desc_stmt = DescribeStatement(dialect.Hive)
        if cls.check_table_exists(hive_engine, database, tablename):
            result_proxy = hive_engine.execute(desc_stmt.get_sql(database, tablename))
            results = result_proxy.fetchall()
            return HiveUtils.parse_describe_results(results)
        else:
            raise TABLE_NOT_FOUND
    
    @classmethod
    def parse_describe_fromatted(cls, desc):
        table_desc = desc[desc['data_type'] == 'transient_lastDdlTime']['comment'].values
        return int(table_desc[0].strip()) 

    @classmethod
    def describe_formatted(cls, hive_engine, database, tablename):
        desc_stmt = DescribeStatement(dialect.Hive, optional = 'FORMATTED')
        if cls.check_table_exists(hive_engine, database, tablename):
            desc = pd.read_sql(desc_stmt.get_sql(database, tablename), hive_engine)
            return HiveUtils.parse_describe_fromatted(desc)
            
              
