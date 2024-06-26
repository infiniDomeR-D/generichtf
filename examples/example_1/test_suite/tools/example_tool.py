from generichtf import TestSuiteView


class ExampleTool:
    def __init__(self, instance_name: str):
        self.instance_name = instance_name

    def use_tool(self):
        print(f"Hello from example_tool: {self.instance_name}")


# TODO: implement register_deconstructor
# noinspection PyUnresolvedReferences
@register_tool('example_tool')
def get_example_tool_instance(view: TestSuiteView, association: str):
    return ExampleTool(association)
