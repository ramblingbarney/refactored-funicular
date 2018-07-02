class Config(object):
    DEBUG = False
    TESTING = False


class ProductionConfig(Config):
    True

class DevelopmentConfig(Config):
    DEBUG = True
    MONGO_DBNAME = 'recipe_buddy'
    MONGO_URI = 'mongodb://recipeapp:Changethis$3d@ds261570.mlab.com:61570/recipe_buddy'

class TestingConfig(Config):
    TESTING = True
    MONGO_DBNAME = 'recipe_buddy'
    MONGO_URI = 'mongodb://recipeapp:Changethis$3d@ds261570.mlab.com:61570/recipe_buddy'
