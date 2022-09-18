from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


@dataclass
class TestEnvironment:
    loaded_tools: List[str] = field(default_factory=list)


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
