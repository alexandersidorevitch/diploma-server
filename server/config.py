from os import path

import errors
from settings import BaseConfig as Config, __absolute_path


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    pass


SERVER_CONFIGS = {
    'develop': DevelopmentConfig,
    'production': ProductionConfig
}

if path.exists(path.join(__absolute_path, '.env.develop')):
    CONFIG = SERVER_CONFIGS['develop']

elif path.exists(path.join(__absolute_path, '.env.prod')):
    CONFIG = SERVER_CONFIGS['production']

else:
    raise errors.ResourceNotFound('.env file wasn\'t found')
