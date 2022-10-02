from os import listdir
from os.path import isdir, isfile, join, split
import importlib.util
import sys
from inspect import isclass
from typing import Callable, List
from dataclasses import dataclass
from threading import Thread

from generichtf.base import ToolFactory, TestEnvironment
from generichtf.exceptions import *


@dataclass
class TestProcedureEntry:
    name: str
    parameters: List
    outputs: List
    procedure: Callable


class ProcedureRunner:
    def __init__(self, procedure_entry: TestProcedureEntry):
        self.procedure_entry = TestProcedureEntry


class TestSuite:
    def _register_procedure(self, name: str, parameters=None, outputs=None):
        parameters = parameters if parameters else []
        outputs = outputs if outputs else []

        def inner_register_procedure(test_function: Callable):
            entry = TestProcedureEntry(name, parameters, outputs, test_function)
            self.procedures[name] = entry
            return test_function

        return inner_register_procedure

    def _register_flow(self, name):

        def inner_register_flow(flow_function: Callable):
            self.flows[name] = flow_function
            return flow_function

        return inner_register_flow

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

    def _load_procedures_file(self, procedures_file_path: str):
        module_name = split(procedures_file_path)[-1].removesuffix('.py')
        spec = importlib.util.spec_from_file_location(module_name, procedures_file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        module.__dict__['register_procedure'] = self._register_procedure

        try:
            # run the module
            spec.loader.exec_module(module)
        except Exception as e:
            raise e

    def _load_flows_file(self, flows_file_path: str):
        module_name = split(flows_file_path)[-1].removesuffix('.py')
        spec = importlib.util.spec_from_file_location(module_name, flows_file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        module.__dict__['register_flow'] = self._register_flow

        try:
            # run the module
            spec.loader.exec_module(module)
        except Exception as e:
            raise e

    @staticmethod
    def _load_module_files(modules_dir_path: str, module_loading_function: Callable):
        module_file_paths = [join(modules_dir_path, filename) for filename in listdir(modules_dir_path) if
                             isfile(join(modules_dir_path, filename))]

        for module_file_path in module_file_paths:
            module_loading_function(module_file_path)

    def __init__(self, root_dir: str):
        self.env = TestEnvironment()
        self.tools = dict()
        self.procedures = dict()
        self.flows = dict()

        dir_list = [dir_name for dir_name in listdir(root_dir) if isdir(join(root_dir, dir_name))]
        assert ('procedures' in dir_list and 'tools' in dir_list and 'flows' in dir_list)

        tools_dir_path = join(root_dir, 'tools')
        self._load_module_files(tools_dir_path, self._load_tool_file)

        procedures_dir_path = join(root_dir, 'procedures')
        self._load_module_files(procedures_dir_path, self._load_procedures_file)

        flows_dir_path = join(root_dir, 'flows')
        self._load_module_files(flows_dir_path, self._load_flows_file)

        pass
