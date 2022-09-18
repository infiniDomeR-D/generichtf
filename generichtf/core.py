from os import listdir
from os.path import isdir, isfile, join, split
import importlib.util
import sys
from inspect import isclass

from generichtf.interfaces import ToolFactory, TestEnvironment
from generichtf.exceptions import *


class TestInstance:
    pass


class TestSuite:
    def _load_tool_file(self, tool_file_path: str):
        module_name = split(tool_file_path)[-1].removesuffix('.py')
        spec = importlib.util.spec_from_file_location(module_name, tool_file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        try:
            # run the module
            spec.loader.exec_module(module)

            # list all tool factories in the module
            module_tools = [item for item in module.__dict__.values() if
                            isclass(item) and issubclass(item, ToolFactory) and item != ToolFactory]

            # add each tool factory instance to the dictionary of tools
            for module_tool in module_tools:
                tool_name = module_tool.get_tool_name()

                if tool_name in self.tools.keys():
                    raise DuplicateToolName

                self.tools[tool_name] = module_tool(self.env)
                self.env.loaded_tools.append(tool_name)

        except Exception as e:
            raise e

    def _load_tool_files(self, tools_dir_path: str):
        tool_file_paths = [join(tools_dir_path, filename) for filename in listdir(tools_dir_path) if
                           isfile(join(tools_dir_path, filename))]

        for tool_file_path in tool_file_paths:
            self._load_tool_file(tool_file_path)

    def __init__(self, root_dir: str):
        self.env = TestEnvironment()
        self.tools = dict()

        dir_list = [dir_name for dir_name in listdir(root_dir) if isdir(join(root_dir, dir_name))]
        assert ('tests' in dir_list and 'tools' in dir_list)

        tests_dir_path = join(root_dir, 'tests')
        tools_dir_path = join(root_dir, 'tools')

        self._load_tool_files(tools_dir_path)
