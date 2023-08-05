import sqlalchemy
import urllib


class Connection(object):

    def __init__(self, host=None, port=1433, database=None, user=None, password=None):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def make_engine(self, conn_string, **kwargs):
        connect_args = kwargs.get('connect_args')
        if connect_args:
            self.engine = sqlalchemy.engine.create_engine(conn_string, connect_args=connect_args)
        else:
            self.engine = sqlalchemy.engine.create_engine(conn_string)


class AzureConnection(Connection):

    ENCRYPT = 'yes'
    TRUST_SERVER_CERT = 'no'
    TIMEOUT = '30'
    PARAM_STRING = 'Driver={{ODBC Driver 17 for SQL Server}};Server=tcp:{HOST},{PORT};Database={DATABASE};Uid={USER};Pwd={PASSWORD};{CONN_CONFIGS}'
    CONNECTION_STRING = "mssql+pyodbc:///?odbc_connect={PARAMS}"
    CONN_CONFIGS = 'Encrypt={ENCRYPT};TrustServerCertificate={TRUST_SERVER_CERT};Connection Timeout={TIMEOUT};'.format(ENCRYPT=ENCRYPT, TRUST_SERVER_CERT=TRUST_SERVER_CERT, TIMEOUT=TIMEOUT)

    def connect(self):
        param_string = AzureConnection.PARAM_STRING.format(
            HOST=self.host,
            PORT=self.port,
            DATABASE=self.database,
            USER=self.user,
            PASSWORD=self.password,
            CONN_CONFIGS=AzureConnection.CONN_CONFIGS
            ) 
        params = urllib.parse.quote_plus(param_string)             
        con_string = AzureConnection.CONNECTION_STRING.format(PARAMS=params)
        self.make_engine(con_string)
        self.engine.connect()
        return self.engine


class HiveConnection(Connection):

    CONNECTION_STRING = 'hive://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'
    
    def connect(self):
        con_string = HiveConnection.CONNECTION_STRING.format(
                    USER=self.user,
                    PASSWORD=self.password,
                    HOST=self.host,
                    PORT=self.port,
                    DATABASE=self.database            
        )
        self.make_engine(con_string, connect_args={'auth': 'LDAP'})
        self.engine.connect()
        return self.engine

class MySqlConnection(Connection):

    CONNECTION_STRING = 'mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'

    def connect(self):
        con_string = MySqlConnection.CONNECTION_STRING.format(
            USER=self.user,
            PASSWORD=self.password,
            HOST=self.host,
            PORT=self.port,
            DATABASE=self.database
        )
        self.make_engine(con_string)
        self.engine.connect()
        return self.engine

