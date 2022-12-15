from abc import ABC, abstractmethod
from typing import Callable, Dict
from enum import Enum, auto, unique
from generichtf.exceptions import *


@unique
class ProcedureStatus(Enum):
    STAGED = auto()
    ONGOING = auto()
    COULD_NOT_COMPLETE = auto()
    DEPENDENCY_EXCEPTION = auto()
    EXCEPTED = auto()
    CRASHED = auto()
    CANCELLED = auto()
    COMPLETED = auto()


class ProcedureHandle:
    def __init__(self, status_function: Callable, result_function: Callable, wait_function: Callable,
                 run_function: Callable, running_time_function: Callable):
        self._status_function = status_function
        self._result_function = result_function
        self._wait_function = wait_function
        self._run_function = run_function
        self._running_time_function = running_time_function

    @property
    def status(self) -> ProcedureStatus:
        return self._status_function()

    @property
    def result(self):
        return self._result_function()

    @property
    def running_time(self):
        return self._running_time_function()

    def wait(self):
        self._wait_function()
        return self

    def run(self):
        if self.status == ProcedureStatus.STAGED:
            self._run_function()
        else:
            raise ProcedureIsNotStaged

        return self


class TestSessionStatus(Enum):
    UNKNOWN = auto()
    COULD_NOT_COMPLETE = auto()
    EXCEPTED = auto()
    COMPLETED = auto()


class TestSession(ABC):

    @property
    @abstractmethod
    def status(self) -> TestSessionStatus:
        pass

    @property
    @abstractmethod
    def parameters(self) -> dict:
        pass

    @property
    @abstractmethod
    def findings(self) -> dict:
        pass

    @abstractmethod
    def stage_procedure(self, procedure_name: str, **parameters) -> ProcedureHandle:
        pass

    @abstractmethod
    def run_flow(self, flow_name: str, merge_findings: bool = True, parameters: None | dict = None):
        pass

    @abstractmethod
    def post_finding(self, name: str, finding: object):
        pass

    @abstractmethod
    def indicate_completion(self):
        pass

    @abstractmethod
    def indicate_non_completion(self):
        pass

    @abstractmethod
    def indicate_exception(self):
        pass

    @abstractmethod
    def log(self, message: str):
        pass


class TestSuiteView(ABC):
    @property
    @abstractmethod
    def configurations(self) -> Dict:
        pass

    @property
    @abstractmethod
    def tools(self) -> Dict:
        pass


class TestReport(ABC):
    pass
