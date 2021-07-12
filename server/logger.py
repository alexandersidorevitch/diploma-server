import logging
import os

from config import CONFIG

LOGGERS = {}


def _get_file_handler(log_file):
    log_file_name = log_file or CONFIG.DEFAULT_LOG_FILE_NAME
    file_handler = logging.FileHandler(os.path.join(CONFIG.LOG_DIR, log_file_name))
    file_handler.setFormatter(logging.Formatter(CONFIG.LOGGER_FORMAT))
    return file_handler


def _get_stream_handler():
    logging.StreamHandler.terminator = '\r\n'
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(CONFIG.LOGGER_FORMAT))
    return stream_handler


def get_logger(name, level=logging.INFO, use_file=False, use_stream=False, log_file=None):

    if name in LOGGERS:
        return LOGGERS[name]

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if use_file:
        file_handler = _get_file_handler(log_file)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)

    if use_stream:
        stream_handler = _get_stream_handler()
        stream_handler.setLevel(level)
        logger.addHandler(stream_handler)

    LOGGERS[name] = logger
    return logger
