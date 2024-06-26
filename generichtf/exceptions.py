class GenericHTFException(Exception):
    pass


class DuplicateToolName(GenericHTFException):
    pass


class DuplicateFunction(GenericHTFException):
    pass


class TestFlowDoesNotExist(GenericHTFException):
    pass


class ProcedureIsNotStaged(GenericHTFException):
    pass
