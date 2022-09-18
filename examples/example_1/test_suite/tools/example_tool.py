from generichtf.interfaces import ToolFactory, TestEnvironment


class ExampleToolFactory(ToolFactory):
    @staticmethod
    def get_tool_name() -> str:
        return 'ex_tool'

    def __init__(self, test_environment: TestEnvironment):
        self.test_environment = test_environment

    def get_instance(self, *args, **kwargs) -> object:
        pass
