class Config(object):
    DEBUG = True


class ProductionConfig(Config):
    True


class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_DBNAME = 'recipe_buddy'
    MONGO_URI = 'mongodb://recipeapp:Changethis$3d@ds261570.mlab.com:61570/recipe_buddy'


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    MONGO_DBNAME = 'recipe_app_testing'
    MONGO_URI = 'mongodb://recipeapptester:changethis5@ds125331.mlab.com:25331/recipe_app_testing'


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
