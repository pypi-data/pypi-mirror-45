import unittest
from atarg import testcase


class ExampleExecutorTest(unittest.TestCase):
    def test_run_test(self):
        self.assertEqual(
                testcase.run_test('15\r\n10', '5', 'tests/A'), ('5', True))
        self.assertEqual(
                testcase.run_test('15\r\n14', '-15', 'tests/A'),
                ('1', False))

    def test_run_tests(self):
        self.assertEqual(testcase.run_tests(
            ['15\r\n10', '0\r\n0', '5\r\n20'],
            ['5', '0', '-15'],
            'tests/A'), True)
        self.assertEqual(testcase.run_tests(
            ['15\r\n10', '2\r\n1', '5\r\n20'],
            ['5\n', '0\n', '-15\n'],
            'tests/A'), False)
