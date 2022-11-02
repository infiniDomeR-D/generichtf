from generichtf.base import TestSession


# noinspection PyUnresolvedReferences
@register_flow('example_flow')
def example_flow(test_session: TestSession):
    handle = test_session.stage_procedure('example_procedure', example_parameter='example parameter value')
    handle.run()
    handle.wait()
