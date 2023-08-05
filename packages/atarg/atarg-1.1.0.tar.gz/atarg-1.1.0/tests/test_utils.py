import unittest
from atarg import utils


class HTMLParserTest(unittest.TestCase):
    def test_fetch_inputs_and_outputs(self):
        self.assertEqual(
                utils.fetch_inputs_and_outputs(
                    'https://beta.atcoder.jp/contests/abc020/tasks/abc020_a',
                    'ABC', 20),
                ['1', 'ABC', '2', 'chokudai'])
        self.assertEqual(
                utils.fetch_inputs_and_outputs(
                    'https://beta.atcoder.jp/contests/abc001/tasks/abc001_1',
                    'ABC', 1),
                ['15\r\n10', '5', '0\r\n0', '0', '5\r\n20', '-15'])
        self.assertEqual(
                utils.fetch_inputs_and_outputs(
                    'https://beta.atcoder.jp/contests/arc057/tasks/arc057_a',
                    'ARC', 57),
                ['1000 300', '4', '6 2', '25', '567876543 0', '1999432123457'])
        self.assertEqual(
                utils.fetch_inputs_and_outputs(
                    'https://beta.atcoder.jp/contests/arc058/tasks/arc058_a',
                    'ARC', 58),
                ['1000 8\r\n1 3 4 5 6 7 8 9', '2000', '9999 1\r\n0', '9999'])
        self.assertEqual(
                utils.fetch_inputs_and_outputs(
                    'https://beta.atcoder.jp/contests/agc001/tasks/agc001_a',
                    'AGC', 1),
                ['2\r\n1 3 1 2', '3',
                    '5\r\n100 1 2 3 14 15 58 58 58 29', '135'])

    def test_translate_task(self):
        self.assertEqual(utils.translate_task('ABC', 19, 'A'), '1')
        self.assertEqual(utils.translate_task('ABC', 20, 'A'), 'a')
        self.assertEqual(utils.translate_task('ARC', 34, 'A'), '1')
        self.assertEqual(utils.translate_task('ARC', 35, 'A'), 'a')
        self.assertEqual(utils.translate_task('AGC', 1, 'A'), 'a')

    def test_compose_task_url(self):
        self.assertEqual(
                utils.compose_task_url('ABC', 20, 'a'),
                'https://beta.atcoder.jp/contests/abc020/tasks/abc020_a')

    def test_compose_submit_url(self):
        self.assertEqual(
                utils.compose_submit_url('ABC', 20),
                'https://atcoder.jp/contests/abc020/submit')


if __name__ == '__main__':
    unittest.main()
