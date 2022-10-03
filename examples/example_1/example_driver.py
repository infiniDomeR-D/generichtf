from generichtf.core import TestSuite

if __name__ == '__main__':
    test_suite = TestSuite('test_suite')

    test_suite.run_flow('example_flow')
