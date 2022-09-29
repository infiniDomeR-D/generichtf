class GenericHTFException(Exception):
    pass


class DuplicateToolName(GenericHTFException):
    pass


class DuplicateFunction(GenericHTFException):
    pass
