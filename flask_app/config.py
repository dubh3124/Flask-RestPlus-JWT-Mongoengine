import logging
import os

class Config(object):
    def __init__(self):
        self.DEBUG = False
        self.TESTING = False
        self.PRODUCTION = False

        self.SECRET_KEY = os.getenv('SECRET_KEY')
        self.JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
        self.JWT_TOKEN_LOCATION=['cookies']
        self.JWT_ACCESS_CSRF_HEADER_NAME = os.getenv('JWT_ACCESS_CSRF_HEADER_NAME')
        self.JWT_COOKIE_CSRF_PROTECT = True
        self.JWT_COOKIE_DOMAIN = os.getenv('JWT_COOKIE_DOMAIN')

        self.LOG_LEVEL = logging.DEBUG
        self.MONGODB_SETTINGS = self.mongo_from_uri(os.getenv("MONGOURL_DEVELOPMENT"))


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

        self.MONGODB_SETTINGS = self.mongo_from_uri(os.getenv('MONGOURL_PRODUCTION'))


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

        self.MONGODB_SETTINGS = self.mongo_from_uri(os.getenv('MONGOURL_TESTING'))

environment = os.getenv('FLASK_ENV', 'DEVELELOPMENT').lower()
# Alternatively this may be easier if you are managing multiple aws servers:
# environment = socket.gethostname().lower()

if environment == 'testing':
    app_config = TestingConfig()
elif environment == 'production':
    app_config = ProductionConfig()
else:
    app_config = DevelopmentConfig()
