from generichtf.base import TestSession


@register_flow('example_flow')
def example_flow(test_session: TestSession):
    test_session.run_procedure('example_procedure')

    test_session.end_session(True)
