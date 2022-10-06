from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Callable
from enum import Enum, auto, unique
from generichtf.exceptions import *


@unique
class ProcedureStatus(Enum):
    STAGED = auto()
    ONGOING = auto()
    COULD_NOT_COMPLETE = auto()
    EXCEPTED = auto()
    CRASHED = auto()
    CANCELLED = auto()
    COMPLETED = auto()


class ProcedureHandle:
    def __init__(self, status_function: Callable, result_function: Callable, wait_function: Callable,
                 run_function: Callable):
        self._status_function = status_function
        self._result_function = result_function
        self._wait_function = wait_function
        self._run_function = run_function

    @property
    def status(self) -> ProcedureStatus:
        return self._status_function()

    @property
    def result(self):
        return self._result_function()

    def wait(self):
        self._wait_function()

    def run(self):
        if self.status == ProcedureStatus.STAGED:
            self._run_function()
        else:
            raise ProcedureIsNotStaged


class TestSession(ABC):
    @abstractmethod
    def stage_procedure(self, procedure_name: str, **parameters) -> ProcedureHandle:
        pass

    @abstractmethod
    def end_session(self, success: bool):
        pass


class TestReport(ABC):
    pass
