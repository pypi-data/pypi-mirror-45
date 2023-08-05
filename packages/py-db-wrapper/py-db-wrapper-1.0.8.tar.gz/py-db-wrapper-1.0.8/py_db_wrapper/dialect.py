

class Dialect(object):

    TYPES = {}
    brackets = False 
    ticks = False
    CREATE_TABLE_TEMPLATE = "CREATE TABLE {SCHEMA}.{TABLE} ({COLUMNS})"

    def __init__(self):
        pass

    def __str__(self):
        return str(self.TYPES)


class Hive(Dialect):

    ticks = True

class Mssql(Dialect):

    brackets = True


class Mysql(Dialect):

    ticks = True      