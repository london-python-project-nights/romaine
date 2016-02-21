import unittest
from tests import common

from romaine.parser.exceptions import (
    MalformedTableError,
)


class TestExamplesParser(unittest.TestCase):
    """
        Test examples gherkin parser functionality of romaine's core.
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

    def test_getting_example_no_input_modification(self):
        """
            Test that getting example doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example on a list containing
        # """[
        #    'Examples:',
        #    '|one|two|',
        #    '|1|2|',
        # ] """
        input_var = [
            'Examples:',
            '|one|two|',
            '|1|2|',
        ]
        parser.section.get_example(input_var)

        # Then my input variable is not modified
        self.assertEqual(
            input_var,
            [
                'Examples:',
                '|one|two|',
                '|1|2|',
            ],
        )

    def test_basic_examples_without_description(self):
        """
            Check we can get examples with no description.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example on a list containing:
        # """[
        #    'Examples:',
        #    '|one|two|',
        #    '|1|2|',
        # ] """
        input_data = [
            'Examples:',
            '|one|two|',
            '|1|2|',
        ]
        result = parser.section.get_example(input_data)

        # Then I see an example containing:
        # one: ["1"]
        # two: ["2"]
        self.assertEqual(
            result,
            {
                'example': {
                    'leading_comments_and_space': [],
                    'trailing_whitespace': [],
                    'description': '',
                    'columns': {
                        'one': ['1'],
                        'two': ['2'],
                    },
                    'table': [
                        ['one', 'two'],
                        ['1', '2'],
                    ],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_basic_examples_with_description(self):
        """
            Check description can be extracted from an example when present.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example on a list containing:
        # """[
        #    'Examples: Our vital test',
        #    '|first|second|',
        #    '|1|2|',
        # ] """
        input_data = [
            'Examples: Our vital test',
            '|first|second|',
            '|1|2|',
        ]
        result = parser.section.get_example(input_data)

        # Then I see an example described as 'Our vital test' containing:
        # first: ["1"]
        # second: ["2"]
        self.assertEqual(
            result,
            {
                'example': {
                    'leading_comments_and_space': [],
                    'trailing_whitespace': [],
                    'description': ' Our vital test',
                    'columns': {
                        'first': ['1'],
                        'second': ['2'],
                    },
                    'table': [
                        ['first', 'second'],
                        ['1', '2'],
                    ],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_malformed_examples_table_causes_exception(self):
        """
            Check that a malformed table throws an exception.
        """

        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example on a list containing:
        # """[
        #    'Examples:',
        #    '|first|second|',
        #    '|1|',
        # ] """
        # Then I see a MalformedTableError
        with self.assertRaises(MalformedTableError):
            parser.section.get_example([
                'Examples:',
                '|first|second|',
                '|1|',
            ])

    def test_examples_with_incomplete_table_raises_exception(self):
        """
            Confirm we see an exception with just table headings.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example on a list containing:
        # """[
        #    'Examples:',
        #    '|one|two|',
        # ] """
        input_data = [
            'Examples:',
            '|one|two|',
        ]
        result = parser.section.get_example(input_data)

        # Then I see an example containing:
        # one: []
        # two: []
        self.assertEqual(
            result,
            {
                'example': {
                    'leading_comments_and_space': [],
                    'trailing_whitespace': [],
                    'description': '',
                    'columns': {
                        'one': [],
                        'two': [],
                    },
                    'table': [
                        ['one', 'two'],
                    ],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_examples_with_leading_comment_and_whitespace_can_be_parsed(self):

        """
            Check that examples with leading comment and whitespace are valid.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example on a list containing:
        # """[
        #    '#Some comment about the test',
        #    '     ',
        #    'Examples: Our vital test',
        #    '|first|second|',
        #    '|1|2|',
        # ] """
        input_data = [
            '#Some comment about the test',
            '     ',
            'Examples: Our vital test',
            '|first|second|',
            '|1|2|',
        ]
        result = parser.section.get_example(input_data)

        # Then I see an example described as 'Our vital test' containing:
        # first: ["1"]
        # second: ["2"]
        # with leading comments and space of: ['#Some comment about the test',
        # '     ']
        self.assertEqual(
            result,
            {
                'example': {
                    'leading_comments_and_space': [
                        '#Some comment about the test',
                        '     ',
                    ],
                    'trailing_whitespace': [],
                    'description': ' Our vital test',
                    'columns': {
                        'first': ['1'],
                        'second': ['2'],
                    },
                    'table': [
                        ['first', 'second'],
                        ['1', '2'],
                    ],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_example_with_trailing_data_and_whitespace(self):
        """
            Check that examples with trailing whitespace and data are valid.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example on a list containing:
        # """[
        #    'Examples: Our vital test',
        #    '|first|second|',
        #    '|1|2|',
        #    '',
        #    'lemons',
        # ] """
        input_data = [
            'Examples: Our vital test',
            '|first|second|',
            '|1|2|',
            '',
            'lemons',
        ]
        result = parser.section.get_example(input_data)

        # Then I see an example described as 'Our vital test' containing:
        # first: ["1"]
        # second: ["2"]
        # with trailing space of: ['']
        # and I have the following lines remaining:
        # ['lemons' ]
        self.assertEqual(
            result,
            {
                'example': {
                    'leading_comments_and_space': [],
                    'trailing_whitespace': [
                        ''
                    ],
                    'description': ' Our vital test',
                    'columns': {
                        'first': ['1'],
                        'second': ['2'],
                    },
                    'table': [
                        ['first', 'second'],
                        ['1', '2'],
                    ],
                },
                'remaining': ['lemons'],
                'raw_input': input_data,
            },
        )

    def test_multiple_examples_sections(self):
        """
            Check that a second example will be left alone.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example on a list containing:
        # """[
        #    'Examples: Our vital test',
        #    '|first|second|',
        #    '|1|2|',
        #    '',
        #    ' Examples: This test is unimportant',
        #    '|first|second|',
        #    '|3|4|',
        # ] """
        input_data = [
            'Examples: Our vital test',
            '|first|second|',
            '|1|2|',
            '',
            ' Examples: This test is unimportant',
            '|first|second|',
            '|3|4|',
        ]
        result = parser.section.get_example(input_data)

        # Then I see an example described as 'Our vital test' containing:
        # first: ["1"]
        # second: ["2"]
        # with trailing space of: ['']
        # and I have the following lines remaining:
        # [ ' Examples: This test is unimportant', '|first|second|',
        #   '|3|4|' ]
        self.assertEqual(
            result,
            {
                'example': {
                    'leading_comments_and_space': [],
                    'trailing_whitespace': [
                        ''
                    ],
                    'description': ' Our vital test',
                    'columns': {
                        'first': ['1'],
                        'second': ['2'],
                    },
                    'table': [
                        ['first', 'second'],
                        ['1', '2']
                    ],
                },
                'remaining': [
                    ' Examples: This test is unimportant',
                    '|first|second|',
                    '|3|4|',
                ],
                'raw_input': input_data,
            },
        )

    def test_no_examples_sections_with_trailing_data(self):
        """
            Check that no examples sections returns no examples.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example on a list containing:
        # [ 'This is not an examples section' ]
        input_data = [
            'This is not an examples section',
        ]
        result = parser.section.get_example(input_data)

        # Then I see no examples section and remaining:
        # [ 'This is not an examples section' ]
        self.assertEqual(
            result,
            {
                'example': None,
                'remaining': ['This is not an examples section'],
                'raw_input': input_data,
            },
        )

    def test_no_examples_sections(self):
        """
            Check that we don't crash trying to get examples from nothing.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example on an empty list
        result = parser.section.get_example([])

        # Then I see no examples section and nothing remaining.
        self.assertEqual(
            result,
            {
                'example': None,
                'remaining': [],
                'raw_input': [],
            },
        )

    def test_examples_divorced_from_table(self):
        """
            Confirm we don't get examples when the table is not attached.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example on a list containing:
        # """[
        #    'Examples:',
        #    '# Misplaced comment',
        #    '|one|two|',
        #    '|1|2|',
        # ] """
        input_data = [
            'Examples:',
            '# Misplaced comment',
            '|one|two|',
            '|1|2|',
        ]
        result = parser.section.get_example(input_data)

        # Then I see no examples section and the remaining: ['Examples:',
        # '# Misplaced comment', '|one|two|', '|1|2|']
        self.assertEqual(
            result,
            {
                'example': None,
                'remaining': [
                    'Examples:',
                    '# Misplaced comment',
                    '|one|two|',
                    '|1|2|',
                ],
                'raw_input': input_data,
            },
        )

    def test_basic_single_examples_without_description(self):
        """
            Check we can get a single example with no description.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_examples on a list containing:
        # """[
        #    'Examples:',
        #    '|one|two|',
        #    '|1|2|',
        # ] """
        input_data = [
            'Examples:',
            '|one|two|',
            '|1|2|',
        ]
        result = parser.section.get_examples(input_data)

        # Then I see one example containing:
        # one: ["1"]
        # two: ["2"]
        self.assertEqual(
            result,
            {
                'examples': [
                    {
                        'leading_comments_and_space': [],
                        'trailing_whitespace': [],
                        'description': '',
                        'columns': {
                            'one': ['1'],
                            'two': ['2'],
                        },
                        'table': [
                            ['one', 'two'],
                            ['1', '2'],
                        ],
                    },
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_multiple_examples_sections(self):
        """
            Check that we can retrieve two examples sections.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_examples on a list containing:
        # """[
        #    'Examples: Our vital test',
        #    '|first|second|',
        #    '|1|2|',
        #    '',
        #    ' Examples: This test is unimportant',
        #    '|first|second|',
        #    '|3|4|',
        # ] """
        input_data = [
            'Examples: Our vital test',
            '|first|second|',
            '|1|2|',
            '',
            ' Examples: This test is unimportant',
            '|first|second|',
            '|3|4|',
        ]
        result = parser.section.get_examples(input_data)

        # Then I see one example described as ' Our vital test' containing:
        # first: ["1"]
        # second: ["2"]
        # with trailing space of: ['']
        # and a second example described as ' This test is unimportant'
        # containing:
        # first: ["3"]
        # second: ["4"]
        self.assertEqual(
            result,
            {
                'examples': [
                    {
                        'leading_comments_and_space': [],
                        'trailing_whitespace': [
                            ''
                        ],
                        'description': ' Our vital test',
                        'columns': {
                            'first': ['1'],
                            'second': ['2'],
                        },
                        'table': [
                            ['first', 'second'],
                            ['1', '2'],
                        ],
                    },
                    {
                        'leading_comments_and_space': [],
                        'trailing_whitespace': [],
                        'description': ' This test is unimportant',
                        'columns': {
                            'first': ['3'],
                            'second': ['4'],
                        },
                        'table': [
                            ['first', 'second'],
                            ['3', '4'],
                        ],
                    },
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_one_example_with_example_following_other_data(self):
        """
            Check that an example not immediately following is left alone.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_examples on a list containing:
        # """[
        #    'Examples: Our vital test',
        #    '|first|second|',
        #    '|1|2|',
        #    '',
        #    'Scenario Outline: Missing steps',
        #    ' Examples: This test is unimportant',
        #    '|first|second|',
        #    '|3|4|',
        # ] """
        input_data = [
            'Examples: Our vital test',
            '|first|second|',
            '|1|2|',
            '',
            'Scenario Outline: Missing steps',
            ' Examples: This test is unimportant',
            '|first|second|',
            '|3|4|',
        ]
        result = parser.section.get_examples(input_data)

        # Then I see one example described as 'Our vital test' containing:
        # first: ["1"]
        # second: ["2"]
        # with trailing space of: ['']
        # and I have the following lines remaining:
        # [ 'Scenario Outline: Missing steps', ' Examples: This test is
        # unimportant', '|first|second|', '|3|4|' ]
        self.assertEqual(
            result,
            {
                'examples': [
                    {
                        'leading_comments_and_space': [],
                        'trailing_whitespace': [
                            ''
                        ],
                        'description': ' Our vital test',
                        'columns': {
                            'first': ['1'],
                            'second': ['2'],
                        },
                        'table': [
                            ['first', 'second'],
                            ['1', '2']
                        ],
                    },
                ],
                'remaining': [
                    'Scenario Outline: Missing steps',
                    ' Examples: This test is unimportant',
                    '|first|second|',
                    '|3|4|',
                ],
                'raw_input': input_data,
            },
        )

    def test_do_not_get_multiple_examples_from_nothing(self):
        """
            Check that we can't get many (any) examples from nothing.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_examples with []
        result = parser.section.get_examples([])

        # Then I see no examples
        self.assertEqual(
            result,
            {
                'examples': [],
                'remaining': [],
                'raw_input': [],
            },
        )

    def test_get_examples_no_input_modification(self):
        """
            Test that getting examples doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_examples on a list containing:
        # """[
        #    'Examples: Our vital test',
        #    '|first|second|',
        #    '|1|2|',
        #    '',
        #    ' Examples: This test is unimportant',
        #    '|first|second|',
        #    '|3|4|',
        # ] """
        input_var = [
            'Examples: Our vital test',
            '|first|second|',
            '|1|2|',
            '',
            ' Examples: This test is unimportant',
            '|first|second|',
            '|3|4|',
        ]
        parser.section.get_examples([
            'Examples: Our vital test',
            '|first|second|',
            '|1|2|',
            '',
            ' Examples: This test is unimportant',
            '|first|second|',
            '|3|4|',
        ])

        # Then my input variable is not modified
        self.assertEqual(
            input_var,
            [
                'Examples: Our vital test',
                '|first|second|',
                '|1|2|',
                '',
                ' Examples: This test is unimportant',
                '|first|second|',
                '|3|4|',
            ],
        )
