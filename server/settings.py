from os import path

from dotenv import dotenv_values

__absolute_path = path.dirname(path.dirname(__file__))
if path.exists(path.join(__absolute_path, '.env.develop')):
    _env = dotenv_values(path.join(__absolute_path, '.env.develop'))

elif path.exists(path.join(__absolute_path, '.env.prod')):
    _env = dotenv_values(path.join(__absolute_path, '.env.prod'))

else:
    _env = {}


class BaseConfig:
    SRC_DIR = path.dirname(path.realpath(__file__))
    SERVER_ADDR = _env.get('SERVER_ADDR', '127.0.0.1')
    SERVER_PORT = int(_env.get('SERVER_PORT', 8888))

    LOG_DIR = path.join(SRC_DIR, 'logs')
    DEFAULT_LOG_FILE_NAME = 'logs'

    RECEIVE_CHUNK_SIZE = 1024

    RESULT_LENGTH_HEADER = 4
    ACTION_LENGTH_HEADER = 4
    MESSAGE_LENGTH_HEADER = 4
    MESSAGE_TYPE_HEADER = 4

    HEADERS_LEN = RESULT_LENGTH_HEADER + MESSAGE_LENGTH_HEADER + MESSAGE_TYPE_HEADER

    LOGGER_FORMAT = "%(asctime)s - [%(levelname)s] -  %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    TIME_FORMAT = '%b %d %Y %I:%M:%S.%f'


print(BaseConfig.SERVER_ADDR)
