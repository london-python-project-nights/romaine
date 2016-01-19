import unittest
from tests import common


class TestStepsParser(unittest.TestCase):
    """
        Test steps gherkin parser functionality of romaine's core.
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

    def test_getting_step_no_input_modification(self):
        """
            Test that getting a step doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step on a list containing
        # """[
        #    '    # Check for empty steps',
        #    '    ',
        #    '    When I call get_step on an empty list',
        # ] """
        input_var = [
            '    # Check for empty steps',
            '    ',
            '    When I call get_step on an empty list',
        ]
        parser.step.get_step(input_var)

        # Then my input variable is not modified
        self.assertEqual(
            input_var,
            [
                '    # Check for empty steps',
                '    ',
                '    When I call get_step on an empty list',
            ],
        )

    def test_getting_raw_step(self):
        """
            Check we can get a step with no surrounding data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step on a list containing
        # """[
        #     'When I call get_step on an empty list'
        # ] """
        input_data = [
            'When I call get_step on an empty list',
        ]
        result = parser.step.get_step(input_data)

        # Then the result is a step with type=When and
        # text='I call get_step on an empty list' and nothing remaining
        self.assertEqual(
            result,
            {
                'step': {
                    'leading_comments_and_space': [],
                    'type': 'When',
                    'text': 'I call get_step on an empty list',
                    'multiline_arg': None,
                    'trailing_whitespace': [],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_getting_commented_step(self):
        """
            Check we can get a step with a leading comment.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step on a list containing
        # """[
        #     '    # Check for empty steps',
        #     '    ',
        #     'When I call get_step on an empty list'
        # ] """
        input_data = [
            '    # Check for empty steps',
            '    ',
            '    When I call get_step on an empty list',
        ]
        result = parser.step.get_step(input_data)

        # Then the result is a step with type=When and
        # text='I call get_step on an empty list',
        # leading_comments_and_space=['    # Check for empty steps',
        # '    '], and nothing remaining
        self.assertEqual(
            result,
            {
                'step': {
                    'leading_comments_and_space': [
                        '    # Check for empty steps',
                        '    ',
                    ],
                    'type': 'When',
                    'text': 'I call get_step on an empty list',
                    'multiline_arg': None,
                    'trailing_whitespace': [],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_step_empty(self):
        """
            Confirm that we get nothing when we don't start with a step.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step on a list containing:
        # """[
        #     'This is not a real step.',
        #     'When I call get_step on an empty list',
        # ] """
        input_data = [
            'This is not a real step.',
            'When I call get_step on an empty list',
        ]
        result = parser.step.get_step(input_data)

        # Then the result is no step, with the original list remaining
        self.assertEqual(
            result,
            {
                'step': None,
                'remaining': [
                    'This is not a real step.',
                    'When I call get_step on an empty list',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_step_with_table(self):
        """
            Confirm that we can get a step with a table.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step on a list containing:
        # """[
        #     'When I call get_step with a table like this',
        #     '|this table|'
        # ] """
        input_data = [
            'When I call get_step with a table like this',
            '|this table|',
        ]
        result = parser.step.get_step(input_data)

        # Then the result is a step of type=When with
        # text='I call get_step with a table like this', and a multiline_arg
        # of type=table with [['this table']], and nothing remaining
        self.assertEqual(
            result,
            {
                'step': {
                    'leading_comments_and_space': [],
                    'type': 'When',
                    'text': 'I call get_step with a table like this',
                    'multiline_arg': {
                        'type': 'table',
                        'data': [['this table']],
                    },
                    'trailing_whitespace': [],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_step_with_pythonish_string(self):
        """
            Confirm that we can get a step with a pythonish string.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step on a list containing:
        # """[
        #     'When I call get_step with a string like this',
        #     '"""'
        #     '    multiline string'
        #     '"""'
        # ] """
        input_data = [
            'When I call get_step with a string like this',
            '"""',
            '    multiline string',
            '"""',
        ]
        result = parser.step.get_step(input_data)

        # Then the result is a step of type=When with
        # text='I call get_step with a string like this', and a multiline_arg
        # of type=multiline_string with ['', '    multiline string', ''],
        # and nothing remaining
        self.assertEqual(
            result,
            {
                'step': {
                    'leading_comments_and_space': [],
                    'type': 'When',
                    'text': 'I call get_step with a string like this',
                    'multiline_arg': {
                        'type': 'multiline_string',
                        'data': ['', '    multiline string', ''],
                    },
                    'trailing_whitespace': [],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_step_with_divorced_multiline_arg(self):
        """
            Confirm get step with no multiline arg, separated by whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step on a list containing:
        # """[
        #     'When I call get_step with a string like this',
        #     '"""'
        #     '    multiline string'
        #     '"""'
        # ] """
        input_data = [
            'When I call get_step with a string like this',
            '',
            '"""',
            '    multiline string',
            '"""',
        ]
        result = parser.step.get_step(input_data)

        # Then the result is a step of type=When with
        # text='I call get_step with a string like this', and
        # trailing_whitespace=[''] and ['"""', '    multiline string', '"""']
        # remaining
        self.assertEqual(
            result,
            {
                'step': {
                    'leading_comments_and_space': [],
                    'type': 'When',
                    'text': 'I call get_step with a string like this',
                    'multiline_arg': None,
                    'trailing_whitespace': [''],
                },
                'remaining': [
                    '"""',
                    '    multiline string',
                    '"""',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_step_with_multiline_arg_and_trailing_whitespace(self):
        """
            Confirm we get a step with multiline arg and trailing whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step on a list containing:
        # """[
        #     'When I call get_step with a string like this',
        #     '"""'
        #     '    multiline string'
        #     '"""'
        #     '',
        #     '  \t',
        # ] """
        input_data = [
            'When I call get_step with a string like this',
            '"""',
            '    multiline string',
            '"""',
            '',
            '  \t',
        ]
        result = parser.step.get_step(input_data)

        # Then the result is a step of type=When with
        # text='I call get_step with a string like this', and a multiline_arg
        # of type=multiline_string with ['', '    multiline string', ''],
        # trailing_whitespace=['', '  \t'], and nothing remaining
        self.assertEqual(
            result,
            {
                'step': {
                    'leading_comments_and_space': [],
                    'type': 'When',
                    'text': 'I call get_step with a string like this',
                    'multiline_arg': {
                        'type': 'multiline_string',
                        'data': ['', '    multiline string', ''],
                    },
                    'trailing_whitespace': ['', '  \t'],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_step_with_trailing_step(self):
        """
            Confirm we get a step with multiline arg and trailing whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step on a list containing:
        # """[
        #     '# Test first step
        #     'When I call get_step with a string like this',
        #     '"""'
        #     '    multiline string'
        #     '"""'
        #     '',
        #     '# Test second step',
        #     '',
        #     'Then I am happy not to see this as a step yet',
        # ] """
        input_data = [
            'When I call get_step with a string like this',
            '"""',
            '    multiline string',
            '"""',
            '',
            '# Test second step',
            '',
            'Then I am happy not to see this as a step yet',
        ]
        result = parser.step.get_step(input_data)

        # Then the result is a step of type=When with
        # text='I call get_step with a string like this', and a multiline_arg
        # of type=multiline_string with ['', '    multiline string', ''],
        # trailing_whitespace=[''], and ['# Test second step', '',
        # 'Then I am happy not to see this as a step yet'] remaining
        self.assertEqual(
            result,
            {
                'step': {
                    'leading_comments_and_space': [],
                    'type': 'When',
                    'text': 'I call get_step with a string like this',
                    'multiline_arg': {
                        'type': 'multiline_string',
                        'data': ['', '    multiline string', ''],
                    },
                    'trailing_whitespace': [''],
                },
                'remaining': [
                    '# Test second step',
                    '',
                    'Then I am happy not to see this as a step yet',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_no_step_from_no_lines(self):
        """
            Confirm that we get no step from no lines.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step on no lines
        result = parser.step.get_step([])

        # Then the result is no step, with the original list remaining
        self.assertEqual(
            result,
            {
                'step': None,
                'remaining': [],
                'raw_input': [],
            },
        )

    def test_fail_to_get_steps(self):
        """
            Confirm we get no steps with leading noise.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_steps on a list containing:
        # """[
        #     'This is not a real step.',
        #     'When I call get_step on an empty list',
        # ] """
        input_data = [
            'This is not a real step.',
            'When I call get_step on an empty list',
        ]
        result = parser.step.get_steps(input_data)

        # Then the result is no steps, with the original list remaining
        self.assertEqual(
            result,
            {
                'steps': [],
                'remaining': [
                    'This is not a real step.',
                    'When I call get_step on an empty list',
                ],
                'raw_input': input_data,
            },
        )

    def test_getting_steps_no_input_modification(self):
        """
            Test that getting steps doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_steps on a list containing
        # """[
        #    'When I call get_step with a string like this',
        #    '"""',
        #    '    multiline string',
        #    '"""',
        #    '',
        #    '# Test second step',
        #    '',
        #    'Then I am happy to see this step',
        #    'No more diagonal lines',
        # ] """
        input_var = [
            'When I call get_step with a string like this',
            '"""',
            '    multiline string',
            '"""',
            '',
            '# Test second step',
            '',
            'Then I am happy to see this step',
            'No more diagonal lines',
        ]
        parser.step.get_steps(input_var)

        # Then my input variable is not modified
        self.assertEqual(
            input_var,
            [
                'When I call get_step with a string like this',
                '"""',
                '    multiline string',
                '"""',
                '',
                '# Test second step',
                '',
                'Then I am happy to see this step',
                'No more diagonal lines',
            ],
        )

    def test_get_steps_single_step(self):
        """
            Confirm we can get a single step when getting steps.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_steps on a list containing:
        # """[
        #     'When I call get_step with a table like this',
        #     '|this table|'
        # ] """
        input_data = [
            'When I call get_step with a table like this',
            '|this table|',
        ]
        result = parser.step.get_steps(input_data)

        # Then the result is a single step of type=When with
        # text='I call get_step with a table like this', and a multiline_arg
        # of type=table with [['this table']], and nothing remaining
        self.assertEqual(
            result,
            {
                'steps': [{
                    'leading_comments_and_space': [],
                    'type': 'When',
                    'text': 'I call get_step with a table like this',
                    'multiline_arg': {
                        'type': 'table',
                        'data': [['this table']],
                    },
                    'trailing_whitespace': [],
                }],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_two_steps(self):
        """
            Confirm we can get two steps.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_steps on a list containing:
        # """[
        #     '# Test first step
        #     'When I call get_step with a string like this',
        #     '"""'
        #     '    multiline string'
        #     '"""'
        #     '',
        #     '# Test second step',
        #     '',
        #     'Then I am happy not to see this as a step yet',
        # ] """
        input_data = [
            'When I call get_step with a string like this',
            '"""',
            '    multiline string',
            '"""',
            '',
            '# Test second step',
            '',
            'Then I am happy to see this step',
            'No more diagonal lines',
        ]
        result = parser.step.get_steps(input_data)

        # Then the result is two steps: type=When with
        # text='I call get_step with a string like this', and a multiline_arg
        # of type=multiline_string with ['', '    multiline string', ''],
        # trailing_whitespace=['']; type=Then with
        # text='I am happy to see this step',
        # leading_comments_and_space of ['# Test second step', ''];
        # and ['No more diagonal lines'] remaining
        self.assertEqual(
            result,
            {
                'steps': [
                    {
                        'leading_comments_and_space': [],
                        'type': 'When',
                        'text': 'I call get_step with a string like this',
                        'multiline_arg': {
                            'type': 'multiline_string',
                            'data': ['', '    multiline string', ''],
                        },
                        'trailing_whitespace': [''],
                    },
                    {
                        'leading_comments_and_space': [
                            '# Test second step',
                            '',
                        ],
                        'type': 'Then',
                        'text': 'I am happy to see this step',
                        'multiline_arg': None,
                        'trailing_whitespace': [],
                    },
                ],
                'remaining': [
                    'No more diagonal lines',
                ],
                'raw_input': input_data,
            },
        )
