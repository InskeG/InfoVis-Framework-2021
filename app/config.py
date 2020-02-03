import os

class Config(object):
    """
    Common configurations
    """
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    """
    Development configurations
    """
    SECRET_KEY = os.urandom(24)
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """
    Testing configurations
    """
    DEBUG = True
    TESTING = True

class StagingConfig(Config):
    """
    Staging configuration
    """
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class ProductionConfig(Config):
    """
    Production configurations
    """


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}
