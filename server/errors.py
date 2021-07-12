from defs import Result


class BaseException(Exception):
    pass


class ResourceNotFound(BaseException):
    RESULT = Result.RESOURCE_NOT_FOUND


class TimeOut(BaseException):
    RESULT = Result.TIMEOUT


class BadCommand(BaseException):
    RESULT = Result.BAD_COMMAND


class InternalServerError(BaseException):
    RESULT = Result.INTERNAL_SERVER_ERROR


all_exceptions = (ResourceNotFound, TimeOut, BadCommand, InternalServerError)


def test():
    raise ResourceNotFound('Jopa')


try:
    test()
except all_exceptions as err:
    print(str(err))
    print(err.RESULT)
