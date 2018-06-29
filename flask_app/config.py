import logging
import os

class Config(object):
    def __init__(self):
        self.DEBUG = False
        self.TESTING = False
        self.PRODUCTION = False

        self.SECRET_KEY = '{SECRET_KEY}'
        self.JWT_SECRET_KEY = '023894239j0fm302m3'
        self.JWT_TOKEN_LOCATION=['cookies']
        self.JWT_ACCESS_CSRF_HEADER_NAME = 'X-XSRF-TOKEN'
        self.JWT_ACCESS_COOKIE_PATH = '/auth'
        self.JWT_COOKIE_CSRF_PROTECT = True
        self.JWT_ACCESS_CSRF_COOKIE_PATH = '/auth'
        self.JWT_COOKIE_DOMAIN = 'dubh3124.com'

        self.LOG_LEVEL = logging.DEBUG
        # Uncomment and fill out for shared DB connection
        self.MONGODB_SETTINGS = self.dbLocation("cloud", username="dubh3124", password="nwQNzyDNoa4G3fox", db_name="mobileapp")

        # # Uncomment and fill out for custom DB coonnection
        # self.MONGODB_SETTINGS = self.dbLocation("custom", db_conn="")




    def dbLocation(self, location, db_conn=None, username=None, password=None, db_name=None):
        if location == "custom":
            uri = db_conn
            return self.mongo_from_uri(uri)
        elif location == "cloud":
            uri = "mongodb://{username}:{password}@bitjobboard-shard-00-00-dyzis.mongodb.net:27017,bitjobboard-shard-00-01-dyzis.mongodb.net:27017,bitjobboard-shard-00-02-dyzis.mongodb.net:27017/{db_name}?ssl=true&replicaSet=bitjobboard-shard-0&authSource=admin&retryWrites=true" \
                .format(username=username, password=password, db_name=db_name)
            return self.mongo_from_uri(uri)
        else:
            raise ValueError('Location must be "custom" or "cloud"')


    @staticmethod
    def mongo_from_uri(uri):
        conn_settings = {
            'host': uri
        }
        return conn_settings


class ProductionConfig(Config):
    def __init__(self):
        super(ProductionConfig, self).__init__()
        self.ENVIRONMENT = 'Production'
        self.PRODUCTION = True
        self.LOG_LEVEL = logging.INFO

        self.MAIL_SERVER = 'smtp.mandrillapp.com'
        self.MAIL_PORT = 465
        self.MAIL_USE_SSL = True
        self.MAIL_USERNAME = os.getenv('MANDRILL_USERNAME')
        self.MAIL_PASSWORD = os.getenv('MANDRILL_APIKEY')

        self.MONGODB_SETTINGS = self.mongo_from_uri('mongodb://bitregistry-user:BIT123@ds111648.mlab.com:11648/heroku_xc23j00v')


class DevelopmentConfig(Config):
    '''
    Use "if app.debug" anywhere in your code,
    that code will run in development mode.
    '''
    def __init__(self):
        super(DevelopmentConfig, self).__init__()
        self.ENVIRONMENT = 'Dev'
        self.DEBUG = True
        self.TESTING = False


class TestingConfig(Config):
    '''
    A Config to use when we are running tests.
    '''
    def __init__(self):
        super(TestingConfig, self).__init__()
        self.ENVIRONMENT = 'Testing'
        self.DEBUG = False
        self.TESTING = True

        self.MONGODB_SETTINGS = self.mongo_from_uri(
            'mongodb://localhost:27017/testing'
        )

environment = os.getenv('ENVIRONMENT', 'DEVELELOPMENT').lower()
# Alternatively this may be easier if you are managing multiple aws servers:
# environment = socket.gethostname().lower()

if environment == 'testing':
    app_config = TestingConfig()
elif environment == 'production':
    app_config = ProductionConfig()
else:
    app_config = DevelopmentConfig()
