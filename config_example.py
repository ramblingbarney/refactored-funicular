import coverage

MONGO_USERNAME = 'recipeapptester'
MONGO_PASSWORD = '<replace>'


class Config(object):
    DEBUG = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_DBNAME = 'recipe_buddy'
    MONGO_URI = 'mongodb://recipeapp:<replace>@ds261570.mlab.com:61570/recipe_buddy'
    SECRET_KEY = '<replace>'


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    coverage.process_startup()
    MONGO_DBNAME = 'recipe_app_testing'
    MONGO_URI = 'mongodb://recipeapptester:<replace>@127.0.0.1:27017/recipe_app_testing'
    SECRET_KEY = '<replace>'


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
