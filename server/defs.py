from enum import IntEnum, auto


class Result(IntEnum):
    OK = auto()
    BAD_COMMAND = auto()
    RESOURCE_NOT_FOUND = auto()
    ACCESS_DENIED = auto()
    TIMEOUT = auto()
    INTERNAL_SERVER_ERROR = auto()


class Action(IntEnum):
    LOGIN = auto()
    LOGOUT = auto()
    GET = auto()


class Type(IntEnum):
    TEXT = auto()
    IMAGE = auto()
    VIDEO = auto()
    MUSIC = auto()
