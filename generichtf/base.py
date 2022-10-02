from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Callable
from enum import Enum, auto, unique


@unique
class ProcedureStatus(Enum):
    ONGOING = auto()
    COULD_NOT_COMPLETE = auto()
    EXCEPTED = auto()
    CRASHED = auto()
    COMPLETED = auto()


@dataclass
class TestEnvironment:
    loaded_tools: List[str] = field(default_factory=list)


class TestSession(ABC):
    @abstractmethod
    def run_procedure(self, procedure_name: str, **parameters):
        pass

    @abstractmethod
    def end_session(self, success: bool):
        pass


class TestReport(ABC):
    pass


class ToolFactory(ABC):

    @abstractmethod
    def __init__(self, test_environment: TestEnvironment):
        pass

    @abstractmethod
    def get_instance(self, *args, **kwargs) -> object:
        pass

    @staticmethod
    @abstractmethod
    def get_tool_name() -> str:
        pass
