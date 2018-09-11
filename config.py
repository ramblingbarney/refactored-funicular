import os

MONGO_USERNAME = 'recipeapptester'
MONGO_PASSWORD = 'changeme5'

class Config(object):
    DEBUG = True


class ProductionConfig(Config):
    True


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_DBNAME = os.getenv('MONGO_DBNAME', None)
    MONGO_URI = os.getenv('MONGO_URI', None)
    SECRET_KEY = os.getenv('SECRET_KEY', None)


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    MONGO_DBNAME = 'recipe_app_testing'
    MONGO_URI = 'mongodb://recipeapptester:changeme5@127.0.0.1:27017/recipe_app_testing'
    SECRET_KEY = 'h0SH15Z>StUzy:a1lQ2vVARVT?jt=xsXGPy0?!P5mN8-deIcoh9x3|e2DxQJuF8hFfBh@gYz3M&$YM$BT&lklDA=mgH1EnD}$|4e'


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
