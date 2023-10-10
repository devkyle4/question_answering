class Config(object):
    DEBUG = False
    TESTING = False
    # Add other global configs


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    # Add other development specific configs


class TestingConfig(Config):
    TESTING = True
    # Add other testing specific configs
