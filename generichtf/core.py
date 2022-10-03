from os import listdir
from os.path import isdir, isfile, join, split
import importlib.util
import sys
from typing import Callable, List
from dataclasses import dataclass
from threading import Thread

from generichtf.base import TestSession, ProcedureHandle, ProcedureStatus
from generichtf.exceptions import *


@dataclass
class TestProcedureEntry:
    name: str
    parameters: List
    outputs: List
    procedure: Callable


class ProcedureRunner:
    def __init__(self, procedure_entry: TestProcedureEntry):
        self.procedure_entry = procedure_entry
        self._status = ProcedureStatus.STAGED
        self._result = None
        self._run_thread = None

    def _get_status(self):
        return self._status

    def _get_result(self):
        return self._result

    def _wait(self):
        pass

    def get_procedure_handle(self) -> ProcedureHandle:
        handle = ProcedureHandle(self._get_status, self._get_result, self._wait)
        return handle

    def run(self):
        def wrapped_function():
            try:
                result = self.procedure_entry.procedure()
            except Exception as e:
                result = e

            self._result = result

        run_thread = Thread(target=wrapped_function)

        self._run_thread = run_thread
        run_thread.start()


class TestSuite:
    def _register_tool(self, name: str):
        def inner_register_tool(tool_instance_function: Callable):
            self.tools[name] = tool_instance_function
            return tool_instance_function

        return inner_register_tool

    def _register_procedure(self, name: str, parameters=None, outputs=None):
        parameters = parameters if parameters else []
        outputs = outputs if outputs else []

        def inner_register_procedure(procedure_function: Callable):
            entry = TestProcedureEntry(name, parameters, outputs, procedure_function)
            self.procedures[name] = entry
            return procedure_function

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
        module.__dict__['register_tool'] = self._register_tool

        try:
            # run the module
            spec.loader.exec_module(module)
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

    def run_flow(self, flow_name: str):
        flow_function = self.flows[flow_name]

        session = MainTestSession(self)

        flow_function(session)

    def __init__(self, root_dir: str):
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


class MainTestSession(TestSession):
    def __init__(self, test_suite: TestSuite):
        self.test_suite = test_suite

    def end_session(self, success: bool):
        pass

    def run_procedure(self, procedure_name: str, **parameters):
        procedure_entry = self.test_suite.procedures[procedure_name]

        runner = ProcedureRunner(procedure_entry)
        runner.run()
