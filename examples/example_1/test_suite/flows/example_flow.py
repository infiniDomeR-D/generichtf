from generichtf.base import TestSession


@register_flow('example_flow')
def example_flow(test_session: TestSession):
    pass

    test_session.end_session(True)
