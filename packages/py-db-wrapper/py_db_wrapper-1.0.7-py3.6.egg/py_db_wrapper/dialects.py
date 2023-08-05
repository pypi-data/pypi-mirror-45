

class Dialect(object):

    TYPES = {}

    def __init__(self):
        pass

    def __str__(self):
        return str(self.TYPES)


class Hive(Dialect):

    GENERIC_TYPES = {}

class Mssql(Dialect):

    TYPES = {}

class Mysql(Dialect):

    TYPES = {}        