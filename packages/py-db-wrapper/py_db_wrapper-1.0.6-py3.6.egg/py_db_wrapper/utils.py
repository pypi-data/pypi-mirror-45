import datetime
import pandas as pd
import logging
import os
import collections
import re
from py_db_wrapper import sqlType
from py_db_wrapper import dialect
from py_db_wrapper.exceptions import TABLE_NOT_FOUND

class HiveUtils(object):

    @staticmethod
    def check_table_exists(hive_engine, database, tablename):
        query = "show tables in {db} like '{tb}'".format(db=database,tb=tablename)
        res = pd.read_sql(query, hive_engine)
        if len(res.index) > 0:
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
        if cls.check_table_exists(hive_engine, database, tablename):
            sql_string = 'describe {db}.{tb}'.format(db=database,tb=tablename)
            result_proxy = hive_engine.execute(sql_string)
            results = result_proxy.fetchall()
            return HiveUtils.parse_describe_results(results)
        else:
            raise TABLE_NOT_FOUND
