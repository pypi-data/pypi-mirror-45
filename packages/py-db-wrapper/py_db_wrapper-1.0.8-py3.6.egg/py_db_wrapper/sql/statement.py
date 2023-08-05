from py_db_wrapper.exceptions import STATEMENT_EXCEPTION

class Statement:

    TEMPLATE = ""

    def __init__(self, dialect):
        self.dialect = dialect

    def add_ticks_and_brackets(self, string):
        if self.dialect.brackets and not self.dialect.ticks:
            return '[{}]'.format(string)
        elif self.dialect.ticks and not self.dialect.brackets:
            return '`{}`'.format(string)
        elif self.dialect.ticks and self.dialect.brackets:
            return '[`{}`]'.format(string)
        else:
            return string

    def build_sql(self, **kwargs):
        return self.TEMPLATE.format(**kwargs)

class CreateTableStatement(Statement):

    TEMPLATE = 'CREATE TABLE {schema}.{table} ({columns})'

    def __init__(self, dialect, columns=None):
        """
        kwargs:-
            columns. A tuple list like [(string, SqlType), (string, SqlType)]
        """
        super().__init__(dialect)
        self.columns = columns

    def process_columns(self):
        vals = ['{} {}'.format(
            self.add_ticks_and_brackets(name),
            sql_type.sql_string(self.dialect)
            ) 
            for name, sql_type in self.columns]

        return ', '.join(vals)

    def get_sql(self, schema, table): 
        if self.columns:       
            columns = self.process_columns()
            schema = self.add_ticks_and_brackets(schema)
            table = self.add_ticks_and_brackets(table)
            return self.build_sql(schema=schema, table=table, columns=columns)  
        else:
            raise STATEMENT_EXCEPTION 

class DescribeStatement(Statement):

    TEMPLATE = 'DESCRIBE {optional} {schema}.{table}' 

    def __init__(self, dialect, optional=''):
        """
        kwargs:-
            columns. A tuple list like [(string, SqlType), (string, SqlType)]
        """
        super().__init__(dialect)
        self.optional = optional   

    def get_sql(self, schema, table): 
        schema = self.add_ticks_and_brackets(schema)
        table = self.add_ticks_and_brackets(table)        
        return self.build_sql(optional=self.optional, schema=schema, table=table)

class ShowTablesStatement(Statement):

    TEMPLATE = 'SHOW TABLES IN {schema}' 

    def __init__(self, dialect, optional=''):
        """
        kwargs:-
            columns. A tuple list like [(string, SqlType), (string, SqlType)]
        """
        super().__init__(dialect)
        self.optional = optional   

    def get_sql(self, schema): 
        schema = self.add_ticks_and_brackets(schema)       
        return self.build_sql(schema=schema)        