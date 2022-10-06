# noinspection PyUnresolvedReferences
@associate_tool('example_tool', 'example association')
@register_procedure('example_procedure')
def example_procedure(example_tool, **kwargs):
    print("Hi from example_procedure")
    print(f"My parameters: {kwargs}")
    example_tool.use_tool()
