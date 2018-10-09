import os


class Config(object):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False

    MONGO_DBNAME = os.environ['MONGO_DBNAME']
    MONGO_URI = os.environ['MONGO_URI']
    SECRET_KEY = os.environ['SECRET_KEY']


class DevelopmentConfig(Config):
    DEBUG = False

    MONGO_DBNAME = os.environ['MONGO_DBNAME']
    MONGO_URI = os.environ['MONGO_URI']
    SECRET_KEY = os.environ['SECRET_KEY']


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}
