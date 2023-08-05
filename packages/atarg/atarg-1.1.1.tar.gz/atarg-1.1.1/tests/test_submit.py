import unittest
from atarg import submit

class SubmitExecutorTest(unittest.TestCase):
    def test_extract_by_name(self):
        html_text = '''
        <html>
            <head>
                <title> Yo </title>
            </head>
            <body>
                <input type="hidden" name="test1" value="1">
                <input type="hidden" name="test2" value="2">
            </body>
        </html>
        '''
        self.assertEqual(
                submit.extract_by_name(html_text, 'test1'),
                '1')
