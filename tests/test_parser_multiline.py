import unittest
from tests import common

from romaine.parser.exceptions import UnclosedPythonishString


class TestMultilineParser(unittest.TestCase):
    """
        Test multi-line gherkin parser functionality of romaine's core.
    """
    def setUp(self):
        """
            Prepare the environment for testing.
        """
        # We're doing a lot of long tests- don't limit the diff output length
        self.maxDiff = None

    def tearDown(self):
        """
            Revert changes made during testing.
        """
        pass

    def test_getting_pythonish_string_no_input_modification(self):
        """
            Test that getting a pythonish string doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string on a list containing
        # """['"""',
        #  'this',
        #  'is a',
        #  'test',
        #  '"""',
        # ] """
        input_var = [
            '"""',
            'this',
            'is a',
            'test',
            '"""',
        ]
        parser.multiline.get_pythonish_string(input_var)

        # Then my input variable is not modified
        self.assertEqual(
            input_var,
            [
                '"""',
                'this',
                'is a',
                'test',
                '"""',
            ],
        )

    def test_getting_pythonish_string(self):
        """
            Check we can get a pythonish string.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string on a list containing
        # """['"""',
        #  'this',
        #  'is a',
        #  'test',
        #  '"""',
        # ] """
        input_data = [
            '"""',
            'this',
            'is a',
            'test',
            '"""',
        ]
        result = parser.multiline.get_pythonish_string(input_data)

        # Then the result is a pythonish string of ['', 'this', 'is a',
        # 'test', ''] with nothing remaining
        self.assertEqual(
            result,
            {
                'pythonish_string': ['', 'this', 'is a', 'test', ''],
                'remaining': [],
                'raw_input': input_data,
            }
        )

    def test_getting_pythonish_string_with_delimiter_noise(self):
        """
            Check we can get a pythonish string with noise by the delimiters
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string on a list containing
        # """['"""this',
        #  'is a',
        #  'test"""',
        # ] """
        input_data = [
            '"""this',
            'is a',
            'test"""',
        ]
        result = parser.multiline.get_pythonish_string(input_data)

        # Then the result is a pythonish string of ['this', 'is a', 'test']
        # with nothing remaining
        self.assertEqual(
            result,
            {
                'pythonish_string': ['this', 'is a', 'test'],
                'remaining': [],
                'raw_input': input_data,
            }
        )

    def test_getting_pythonish_string_with_trailing_data(self):
        """
            Check we can get a pythonish string with noise by the delimiters
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string on a list containing
        # """['"""this',
        #  'is a',
        #  'test"""',
        #  'not',
        #  'today',
        # ] """
        input_data = [
            '"""this',
            'is a',
            'test"""',
            'not',
            'today',
        ]
        result = parser.multiline.get_pythonish_string(input_data)

        # Then the result is a pythonish string of ['this', 'is a', 'test']
        # with nothing remaining
        self.assertEqual(
            result,
            {
                'pythonish_string': ['this', 'is a', 'test'],
                'remaining': ['not', 'today'],
                'raw_input': input_data,
            }
        )

    def test_fail_getting_single_quoted_pythonish_string(self):
        """
            Check we do not get a pythonish string with '''.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string on a list containing
        # """["'''",
        #  'this',
        #  'is a',
        #  'test',
        #  "'''",
        # ] """
        input_data = [
            "'''",
            'this',
            'is a',
            'test'
            "'''",
        ]
        result = parser.multiline.get_pythonish_string(input_data)

        # Then there is no pythonish string and the same input list remaining
        self.assertEqual(
            result,
            {
                'pythonish_string': None,
                'remaining': [
                    "'''",
                    'this',
                    'is a',
                    'test'
                    "'''",
                ],
                'raw_input': input_data,
            }
        )

    def test_fail_getting_not_following_pythonish_string(self):
        """
            Check we do not get a pythonish string with a leading line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string on a list containing
        # """['',
        #  '"""',
        #  'this',
        #  'is a',
        #  'test',
        #  '"""',
        # ] """
        input_data = [
            '',
            '"""',
            'this',
            'is a',
            'test'
            '"""',
        ]
        result = parser.multiline.get_pythonish_string(input_data)

        # Then there is no pythonish string and the same input list remaining
        self.assertEqual(
            result,
            {
                'pythonish_string': None,
                'remaining': [
                    '',
                    '"""',
                    'this',
                    'is a',
                    'test'
                    '"""',
                ],
                'raw_input': input_data,
            }
        )

    def test_fail_getting_unclosed_pythonish_string(self):
        """
            Check we fail noisily on an unclosed pythonish string.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string on a list containing
        # """['"""',
        #  'this',
        #  'is a',
        #  'test',
        # ] """
        # Then an UnclosedPythonishString exception is raised
        with self.assertRaises(UnclosedPythonishString):
            parser.multiline.get_pythonish_string([
                '"""',
                'this',
                'is a',
                'test'
            ])

    def test_fail_getting_last_line_opening_pythonish_string(self):
        """
            Check we fail noisily when last line is opening python string.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string on a list containing ['"""']
        # Then an UnclosedPythonishString exception is raised
        with self.assertRaises(UnclosedPythonishString):
            parser.multiline.get_pythonish_string(['"""'])

    def test_getting_table_no_input_modification(self):
        """
            Test that getting a table doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_table on a list containing
        # """[
        #     '|my_table_here|more_cells|',
        #     '|yes|',
        #     '|look|for|cells|',
        # ] """
        input_var = [
            '|my_table_here|more_cells|',
            '|yes|',
            '|look|for|cells|',
        ]
        parser.multiline.get_table(input_var)

        # Then my input variable is not modified
        self.assertEqual(
            input_var,
            [
                '|my_table_here|more_cells|',
                '|yes|',
                '|look|for|cells|',
            ],
        )

    def test_get_one_row_one_cell_table(self):
        """
            Test that we can get a table consisting of one row with one cell.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_table on a list containing ['|my_table_here|']
        input_data = [
            '|my_table_here|',
        ]
        result = parser.multiline.get_table(input_data)

        # Then there is a table consisting of [['my_table_here']] and nothing
        # remaining
        self.assertEqual(
            result,
            {
                'table': [['my_table_here']],
                'remaining': [],
                'raw_input': input_data,
            }
        )

    def test_get_one_row_multi_cell_table(self):
        """
            Test that we can get a table consisting of one rwo with two cells.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_table on a list containing
        # ['|my_table_here|more_cells|']
        input_data = [
            '|my_table_here|more_cells|'
        ]
        result = parser.multiline.get_table(input_data)

        # Then there is a table consisting of
        # [['my_table_here', 'more_cells']] and nothing remaining
        self.assertEqual(
            result,
            {
                'table': [['my_table_here', 'more_cells']],
                'remaining': [],
                'raw_input': input_data,
            }
        )

    def test_get_multi_row_multi_cell_table(self):
        """
            Test that we can get a table consisting of multiple rows.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_table on a list containing
        # ['|my_table_here|more_cells|', '|yes|', '|look|for|cells|']
        input_data = [
            '|my_table_here|more_cells|',
            '|yes|',
            '|look|for|cells|'
        ]
        result = parser.multiline.get_table(input_data)

        # Then there is a table consisting of [['my_table_here','more_cells'],
        # ['yes'], ['look', 'for', 'cells']] and nothing remaining
        self.assertEqual(
            result,
            {
                'table': [['my_table_here', 'more_cells'],
                          ['yes'],
                          ['look', 'for', 'cells']],
                'remaining': [],
                'raw_input': input_data,
            }
        )

    def test_get_table_with_trailing_data(self):
        """
            Test that we can get a table consisting of multiple rows.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_table on a list containing
        # ['|my_table_here|more_cells|', '|yes|', '|look|for|cells|',
        #  'no more table', 'ending', '|not|part|of|this|table']
        input_data = [
            '|my_table_here|more_cells|',
            '|yes|',
            '|look|for|cells|',
            'no more table',
            'ending',
            '|not|part|of|this|table|'
        ]
        result = parser.multiline.get_table(input_data)

        # Then there is a table consisting of [['my_table_here','more_cells'],
        # ['yes'], ['look', 'for', 'cells']] and ['no more table', 'ending',
        # '|not|part|of|this|table|'] remaining
        self.assertEqual(
            result,
            {
                'table': [['my_table_here', 'more_cells'],
                          ['yes'],
                          ['look', 'for', 'cells']],
                'remaining': ['no more table',
                              'ending',
                              '|not|part|of|this|table|'],
                'raw_input': input_data,
            }
        )

    def test_fail_to_get_table(self):
        """
            Confirm we cannot get a table when we do not start with a row.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_table on a list containing
        # ['', '|my_table_here|']
        input_data = [
            '',
            '|my_table_here|',
        ]
        result = parser.multiline.get_table(input_data)

        # Then there is no table and ['', '|my_table_here|'] remaining
        self.assertEqual(
            result,
            {
                'table': None,
                'remaining': ['', '|my_table_here|'],
                'raw_input': input_data,
            }
        )

    def test_getting_multiline_arg_no_input_modification(self):
        """
            Test that getting a multiline arg doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_multiline_arg on a list containing
        # """[
        #     '|my_table_here|more_cells|',
        #     '|yes|',
        #     '|look|for|cells|',
        # ] """
        input_var = [
            '|my_table_here|more_cells|',
            '|yes|',
            '|look|for|cells|',
        ]
        parser.multiline.get_multiline_arg(input_var)

        # Then my input variable is not modified
        self.assertEqual(
            input_var,
            [
                '|my_table_here|more_cells|',
                '|yes|',
                '|look|for|cells|',
            ],
        )

    def test_get_multiline_arg_table(self):
        """
            Check we can get a table as a multiline arg.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_multiline_arg on a list containing
        # ['|my_table_here|', '"""', 'not this', '"""']
        input_data = [
            '|my_table_here|',
            '"""',
            'not this',
            '"""',
        ]
        result = parser.multiline.get_multiline_arg(input_data)

        # Then the arg is a table containing ['my_table_here'] and ['"""',
        # 'not this', '"""'] is remaining
        self.assertEqual(
            result,
            {
                'type': 'table',
                'data': [['my_table_here']],
                'remaining': ['"""', 'not this', '"""'],
                'raw_input': input_data,
            }
        )

    def test_get_multiline_arg_pythonish_string(self):
        """
            Check we can get a pythonish string as a multiline arg.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_multiline_arg on a list containing
        # ['"""', 'my pystring', '"""', '|not this|']
        input_data = [
            '"""',
            'my pystring',
            '"""',
            '|not this|',
        ]
        result = parser.multiline.get_multiline_arg(input_data)

        # Then the arg is a multiline string containing ['', 'my pystring',
        # ''] and ['|not this|'] is remaining
        self.assertEqual(
            result,
            {
                'type': 'multiline_string',
                'data': ['', 'my pystring', ''],
                'remaining': ['|not this|'],
                'raw_input': input_data,
            }
        )

    def test_get_no_multiline_arg(self):
        """
            Confirm we get nothing when no multiline arg is following.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_multiline_arg on a list containing
        # ['', '"""', 'my pystring', '"""', '|not this|']
        input_data = [
            '',
            '"""',
            'my pystring',
            '"""',
            '|not this|',
        ]
        result = parser.multiline.get_multiline_arg(input_data)

        # Then there is no multiline arg, and ['', '"""', 'my pystring',
        # '"""', '|not this|'] is remaining
        self.assertEqual(
            result,
            {
                'type': None,
                'data': None,
                'remaining': ['',
                              '"""',
                              'my pystring',
                              '"""',
                              '|not this|'],
                'raw_input': input_data,
            }
        )

    def test_getting_leading_comment_no_input_modification(self):
        """
            Test that getting leading comments doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space on a list containing
        # """[
        #    '# Happy comment',
        #    '',
        # ] """
        input_var = [
            '# Happy comment',
            '',
        ]
        parser.multiline.get_comments_with_space(input_var)

        # Then my input variable is not modified
        self.assertEqual(
            input_var,
            [
                '# Happy comment',
                '',
            ],
        )

    def test_get_leading_comment_with_blank_line(self):
        """
            Check we can get a leading comment with following blank line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space on a list containing
        # [
        #     '# Happy comment',
        #     '',
        # ]
        input_data = [
            '# Happy comment',
            '',
        ]
        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the following leading lines: ['# Happy comment', ''] and
        # no remaining lines
        self.assertEqual(
            result,
            {
                'comments_and_space': [
                    '# Happy comment',
                    '',
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_leading_comment_without_space(self):
        """
            Check we can get a leading comment with no following whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space on a list containing
        # [
        #     '# Happy comment',
        # ]
        input_data = [
            '# Happy comment',
        ]
        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the following leading lines: ['# Happy comment'] and
        # no remaining lines
        self.assertEqual(
            result,
            {
                'comments_and_space': [
                    '# Happy comment',
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_leading_comment_with_trailing_data(self):
        """
            Check we can get a leading comment with trailing data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space on a list containing
        # [
        #     '# Happy comment',
        #     'I like tests',
        # ]
        input_data = [
            '# Happy comment',
            'I like tests',
        ]
        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the following leading lines: ['# Happy comment'] and
        # remaining: ['I like tests']
        self.assertEqual(
            result,
            {
                'comments_and_space': [
                    '# Happy comment',
                ],
                'remaining': [
                    'I like tests'
                ],
                'raw_input': input_data,
            },
        )

    def test_get_leading_comment_with_whitespace(self):
        """
            Check we can get a leading comment with following whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space on a list containing
        # [
        #     '# Happy comment',
        #     '   \t  ',
        # ]
        input_data = [
            '# Happy comment',
            '   \t  ',
        ]
        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the following leading lines: ['# Happy comment',
        # '   \t  '] and no remaining lines
        self.assertEqual(
            result,
            {
                'comments_and_space': [
                    '# Happy comment',
                    '   \t  ',
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_leading_comment_with_whitespace_and_trailing_data(self):
        """
            Check we can get a leading comment with following space and data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space on a list containing
        # [
        #     '# Happy comment',
        #     '   \t  ',
        #     'More tests',
        # ]
        input_data = [
            '# Happy comment',
            '   \t  ',
            'More tests',
        ]
        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the following leading lines: ['# Happy comment',
        # '   \t  '] and remaining: ['More tests']
        self.assertEqual(
            result,
            {
                'comments_and_space': [
                    '# Happy comment',
                    '   \t  ',
                ],
                'remaining': [
                    'More tests',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_leading_comments(self):
        """
            Check we can get multiple leading comments.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space on a list containing
        # [
        #     '# Happy comment',
        #     '# Sad comment',
        # ]
        input_data = [
            '# Happy comment',
            '# Sad comment',
        ]
        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the following leading lines: ['# Happy comment',
        # '# Sad comment'] and no remaining lines
        self.assertEqual(
            result,
            {
                'comments_and_space': [
                    '# Happy comment',
                    '# Sad comment',
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_comments_with_space_and_trailing_data(self):
        """
            Check we can get leading comments and space with trailing data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space on a list containing
        # [
        #     '# Happy comment',
        #     '# Sad comment',
        #     '',
        #     'Another test',
        # ]
        input_data = [
            '# Happy comment',
            '# Sad comment',
            '',
            'Another test',
        ]
        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the following leading lines: ['# Happy comment',
        # '# Sad comment', ''] and remaining: ['Another test']
        self.assertEqual(
            result,
            {
                'comments_and_space': [
                    '# Happy comment',
                    '# Sad comment',
                    '',
                ],
                'remaining': [
                    'Another test',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_leading_comments_with_multiple_trailing_lines(self):
        """
            Check we can get leading comments with multiple trailing lines.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space on a list containing
        # [
        #     '# Happy comment',
        #     'Another test',
        #     'Second line',
        # ]
        input_data = [
            '# Happy comment',
            'Another test',
            'Second line',
        ]
        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the following leading lines: ['# Happy comment']
        # and remaining: ['Another test', 'Second line']
        self.assertEqual(
            result,
            {
                'comments_and_space': [
                    '# Happy comment',
                ],
                'remaining': [
                    'Another test',
                    'Second line',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_leading_comments_space_separated_with_trailing_data(self):
        """
            Check we can get leading comments and spaces, and trailing data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space on a list containing
        # [
        #     '# Happy comment',
        #     '',
        #     '# Sad comment',
        #     '',
        #     'Another test',
        # ]
        input_data = [
            '# Happy comment',
            '',
            '# Sad comment',
            '',
            'Another test',
        ]
        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the following leading lines: ['# Happy comment', '',
        # '# Sad comment', ''] and remaining: ['Another test']
        self.assertEqual(
            result,
            {
                'comments_and_space': [
                    '# Happy comment',
                    '',
                    '# Sad comment',
                    '',
                ],
                'remaining': [
                    'Another test',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_no_leading_comments_with_leading_space(self):
        """
            Confirm we cannot get a leading comment preceded by a blank line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space on a list containing
        # [
        #     '',
        #     '# Happy comment',
        # ]
        input_data = [
            '',
            '# Happy comment',
        ]
        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the following no leading lines, and remaining:  ['',
        # '# Happy comment']
        self.assertEqual(
            result,
            {
                'comments_and_space': [],
                'remaining': [
                    '',
                    '# Happy comment',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_no_leading_comments_with_leading_noise(self):
        """
            Confirm we cannot get a leading comment preceded data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space on a list containing
        # [
        #     'This is not a comment',
        #     '# Happy comment',
        # ]
        input_data = [
            'This is not a comment',
            '# Happy comment',
        ]
        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the following no leading lines, and remaining:
        # ['This is not a comment', '# Happy comment']
        self.assertEqual(
            result,
            {
                'comments_and_space': [],
                'remaining': [
                    'This is not a comment',
                    '# Happy comment',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_no_leading_comments_from_no_lines(self):
        """
            Confirm we cannot get a leading comment from nothing.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space on an empty list
        result = parser.multiline.get_comments_with_space([])

        # Then I see the following no leading lines, and no remaining lines
        self.assertEqual(
            result,
            {
                'comments_and_space': [],
                'remaining': [],
                'raw_input': [],
            },
        )

    def test_getting_space_no_input_modification(self):
        """
            Test that getting space doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_space on a list containing
        # """[
        #    ' \t  ',
        #    '',
        #    'left behind',
        # ] """
        input_var = [
            ' \t  ',
            '',
            'left behind',
        ]
        parser.multiline.get_space(input_var)

        # Then my input variable is not modified
        self.assertEqual(
            input_var,
            [
                ' \t  ',
                '',
                'left behind',
            ],
        )

    def test_get_space_non_whitespace(self):
        """
            Confirm that we get no whitespace from a non space line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_space on a list containing ['bar']
        input_data = [
            'bar',
        ]
        result = parser.multiline.get_space(input_data)

        # Then I see no space and ['bar'] remaining
        self.assertEqual(
            result,
            {
                'space': [],
                'remaining': [
                    'bar',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_space_non_whitespace_then_space(self):
        """
            Confirm that we get no whitespace from a starting non space line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_space on a list containing ['bar', '']
        input_data = [
            'bar',
            '',
        ]
        result = parser.multiline.get_space(input_data)

        # Then I see no space and ['bar', ''] remaining
        self.assertEqual(
            result,
            {
                'space': [],
                'remaining': [
                    'bar',
                    '',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_space_blank_line(self):
        """
            Confirm that we get a blank line as space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_space on a list containing ['']
        input_data = [
            '',
        ]
        result = parser.multiline.get_space(input_data)

        # Then I see [''] space and no remaining
        self.assertEqual(
            result,
            {
                'space': [
                    '',
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_space_whitespace_line(self):
        """
            Confirm that we get a whitespace line as space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_space on a list containing [' \t  ']
        input_data = [
            ' \t  ',
        ]
        result = parser.multiline.get_space(input_data)

        # Then I see [' \t  '] space and no remaining
        self.assertEqual(
            result,
            {
                'space': [
                    ' \t  ',
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_space_whitespace_and_blank_line(self):
        """
            Confirm that we get a whitespace and blank line as space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_space on a list containing [' \t  ', '']
        input_data = [
            ' \t  ',
            '',
        ]
        result = parser.multiline.get_space(input_data)

        # Then I see [' \t  ', ''] space and no remaining
        self.assertEqual(
            result,
            {
                'space': [
                    ' \t  ',
                    '',
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_space_followed_by_non_space(self):
        """
            Confirm that we get space with remaining non space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_space on a list containing [' \t  ', '',
        # 'left behind']
        input_data = [
            ' \t  ',
            '',
            'left behind',
        ]
        result = parser.multiline.get_space(input_data)

        # Then I see [' \t  ', ''] space and ['left behind'] remaining
        self.assertEqual(
            result,
            {
                'space': [
                    ' \t  ',
                    '',
                ],
                'remaining': [
                    'left behind',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_space_nothing(self):
        """
            Confirm that we get no space from nothing.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_space on an empty list
        result = parser.multiline.get_space([])

        # Then I see no space and no remaining
        self.assertEqual(
            result,
            {
                'space': [],
                'remaining': [],
                'raw_input': [],
            },
        )

    def test_getting_leading_tag_no_input_modification(self):
        """
            Test that getting leading tags doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tags on a list containing
        # """[
        #    '@my_tag',
        #    '',
        # ] """
        input_var = [
            '@my_tag',
            '',
        ]
        parser.multiline.get_tags(input_var)

        # Then my input variable is not modified
        self.assertEqual(
            input_var,
            [
                '@my_tag',
                '',
            ],
        )

    def test_get_leading_tag_with_blank_line(self):
        """
            Check we can get a leading tag with following blank line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tags on a list containing
        # [
        #     '@my_tag',
        #     '',
        # ]
        input_data = [
            '@my_tag',
            '',
        ]
        result = parser.multiline.get_tags(input_data)

        # Then I see the tags: ['my_tag']
        self.assertEqual(
            result,
            {
                'tags': [
                    'my_tag',
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_leading_tag_without_space(self):
        """
            Check we can get a leading tag with no following whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tags on a list containing
        # [
        #     '@my_tag',
        # ]
        input_data = [
            '@my_tag',
        ]
        result = parser.multiline.get_tags(input_data)

        # Then I see the tags: ['my_tag']
        self.assertEqual(
            result,
            {
                'tags': [
                    'my_tag',
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_leading_tag_with_trailing_data(self):
        """
            Check we can get a leading tag with trailing data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tags on a list containing
        # [
        #     '@my_tag',
        #     'I like tests',
        # ]
        input_data = [
            '@my_tag',
            'I like tests',
        ]
        result = parser.multiline.get_tags(input_data)

        # Then I see the tags: ['my_tag'], with ['I like tests'] remaining
        self.assertEqual(
            result,
            {
                'tags': [
                    'my_tag',
                ],
                'remaining': [
                    'I like tests'
                ],
                'raw_input': input_data,
            },
        )

    def test_get_leading_tag_with_whitespace(self):
        """
            Check we can get a leading tag with following whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tags on a list containing
        # [
        #     '@my_tag',
        #     '   \t  ',
        # ]
        input_data = [
            '@my_tag',
            '   \t  ',
        ]
        result = parser.multiline.get_tags(input_data)

        # Then I see the tags: ['my_tag']
        self.assertEqual(
            result,
            {
                'tags': [
                    'my_tag',
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_leading_tag_with_whitespace_and_trailing_data(self):
        """
            Check we can get a leading tag with following space and data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tags on a list containing
        # [
        #     '@my_tag',
        #     '   \t  ',
        #     'More tests',
        # ]
        input_data = [
            '@my_tag',
            '   \t  ',
            'More tests',
        ]
        result = parser.multiline.get_tags(input_data)

        # Then I see the tags: ['my_tag'], with ['More tests'] remaining
        self.assertEqual(
            result,
            {
                'tags': [
                    'my_tag',
                ],
                'remaining': [
                    'More tests',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_leading_tags(self):
        """
            Check we can get multiple leading tags.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tags on a list containing
        # [
        #     '@my_tag',
        #     '@moretag',
        # ]
        input_data = [
            '@my_tag',
            '@moretag',
        ]
        result = parser.multiline.get_tags(input_data)

        # Then I see the tags: ['my_tag', 'moretag']
        self.assertEqual(
            result,
            {
                'tags': [
                    'my_tag',
                    'moretag',
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_tags_and_trailing_data(self):
        """
            Check we can get leading tags and space with trailing data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tags on a list containing
        # [
        #     '@my_tag',
        #     '@moretag',
        #     '',
        #     'Another test',
        # ]
        input_data = [
            '@my_tag',
            '@moretag',
            '',
            'Another test',
        ]
        result = parser.multiline.get_tags(input_data)

        # Then I see the tags: ['my_tag', 'moretag'], with ['Another test']
        # remaining
        self.assertEqual(
            result,
            {
                'tags': [
                    'my_tag',
                    'moretag',
                ],
                'remaining': [
                    'Another test',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_leading_tags_with_multiple_trailing_lines(self):
        """
            Check we can get leading tags with multiple trailing lines.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tags on a list containing
        # [
        #     '@manytagsmakelightshine',
        #     'Another test',
        #     'Second line',
        # ]
        input_data = [
            '@manytagsmakelightshine',
            'Another test',
            'Second line',
        ]
        result = parser.multiline.get_tags(input_data)

        # Then I see the tags: ['manytagsmakelightshine'], with
        # ['Another test', 'Second line'] remaining
        self.assertEqual(
            result,
            {
                'tags': [
                    'manytagsmakelightshine',
                ],
                'remaining': [
                    'Another test',
                    'Second line',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_leading_tags_space_separated_with_trailing_data(self):
        """
            Check we can get leading tags and spaces, and trailing data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tags on a list containing
        # [
        #     '@tagyouareit',
        #     '',
        #     '@tageslicht',
        #     '',
        #     'Another test',
        # ]
        input_data = [
            '@tagyouareit',
            '',
            '@tageslicht',
            '',
            'Another test',
        ]
        result = parser.multiline.get_tags(input_data)

        # Then I see the tags: ['tagyouareit', 'tageslicht'], with
        # ['Another test'] remaining
        self.assertEqual(
            result,
            {
                'tags': [
                    'tagyouareit',
                    'tageslicht',
                ],
                'remaining': [
                    'Another test',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_no_leading_tags_with_leading_space(self):
        """
            Confirm we cannot get a leading tag preceded by a blank line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tags on a list containing
        # [
        #     '',
        #     '# Happy tag',
        # ]
        input_data = [
            '',
            '@my_tag',
        ]
        result = parser.multiline.get_tags(input_data)

        # Then I see no tags, with ['', '@my_tag'] remaining
        self.assertEqual(
            result,
            {
                'tags': [],
                'remaining': [
                    '',
                    '@my_tag',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_no_leading_tags_with_leading_noise(self):
        """
            Confirm we cannot get a leading tag preceded data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tags on a list containing
        # [
        #     'This is not a tag',
        #     '@new_tag',
        # ]
        input_data = [
            'This is not a tag',
            '@new_tag',
        ]
        result = parser.multiline.get_tags(input_data)

        # Then I see no tags, with ['This is not a tag', '@new_tag'] remaining
        self.assertEqual(
            result,
            {
                'tags': [],
                'remaining': [
                    'This is not a tag',
                    '@new_tag',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_no_leading_tags_from_no_lines(self):
        """
            Confirm we cannot get a leading tag from nothing.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tags on an empty list
        result = parser.multiline.get_tags([])

        # Then I see no tags
        self.assertEqual(
            result,
            {
                'tags': [],
                'remaining': [],
                'raw_input': [],
            },
        )
