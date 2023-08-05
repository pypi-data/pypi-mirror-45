import unittest
from py_db_wrapper import sqlType
from py_db_wrapper.sql.statement import *
from py_db_wrapper.dialect import *

class TestStatementMethods(unittest.TestCase):

    def test_add_ticks_and_brackets(self):
        dialect = Dialect()
        statement = Statement(dialect)
        self.assertEqual('a', statement.add_ticks_and_brackets('a'))
        statement.dialect.brackets = True
        statement.dialect.ticks = False
        self.assertEqual('[a]', statement.add_ticks_and_brackets('a'))
        statement.dialect.brackets = False
        statement.dialect.ticks = True
        self.assertEqual('`a`', statement.add_ticks_and_brackets('a'))
        statement.dialect.brackets = True
        statement.dialect.ticks = True
        self.assertEqual('[`a`]', statement.add_ticks_and_brackets('a'))

class TestCreateStatememtMethods(unittest.TestCase):

    def test_process_columns(self):
        statement = CreateTableStatement(Mssql)
        statement.columns = [
            ('id', sqlType.INTEGER()),
            ('name', sqlType.STRING(size=10)),
            ('value', sqlType.DECIMAL(size ='1,13'))
            ]
        self.assertEqual('[id] int, [name] varchar(10), [value] decimal(1,13)', statement.process_columns())

    def test_get_sql_mssql(self):
        stmt = CreateTableStatement(Mysql)
        columns = [
            ('id', sqlType.INTEGER()),
            ('name', sqlType.STRING(size=10)),
            ('value', sqlType.DECIMAL(size ='1,13')),
            ('truefalse', sqlType.BOOLEAN())
            ]
        stmt.columns = columns
        sql = stmt.get_sql('foo','bar')       
        expected_sql = "CREATE TABLE `foo`.`bar` (`id` INT, `name` VARCHAR(10), `value` DECIMAL(1,13), `truefalse` BOOLEAN)"
        self.assertEqual(expected_sql, sql)
        

