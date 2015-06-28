import unittest
from tests import common


class TestBackgroundsParser(unittest.TestCase):
    """
        Test backgrounds gherkin parser functionality of romaine's core.
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

    def test_getting_background_no_input_modification(self):
        """
            Test that getting scenario doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background on a list containing
        # """[
        #    'Background:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_var = [
            'Background:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        parser.section.get_background(input_var)

        # Then my input variable is not modified
        self.assertEqual(
            input_var,
            [
                'Background:',
                'Given a paperback book',
                'When I look at the back cover',
                'Then I see the blurb',
            ],
        )

    def test_basic_background(self):
        """
            Check we can get basic backgrounds.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background on a list containing
        # """[
        #    'Background:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            'Background:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_background(input_data)

        # Then I see a background with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # and the original input returned
        self.assertEqual(
            result,
            {
                'background': {
                    'description': '',
                    'leading_comments_and_space': [],
                    'steps': [
                        {
                            'leading_comments_and_space': [],
                            'type': 'Given',
                            'text': 'a paperback book',
                            'multiline_arg': None,
                            'trailing_whitespace': [],
                        },
                        {
                            'leading_comments_and_space': [],
                            'type': 'When',
                            'text': 'I look at the back cover',
                            'multiline_arg': None,
                            'trailing_whitespace': [],
                        },
                        {
                            'leading_comments_and_space': [],
                            'type': 'Then',
                            'text': 'I see the blurb',
                            'multiline_arg': None,
                            'trailing_whitespace': [],
                        },
                    ],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_background_without_steps(self):
        """
            Check we can get a background without steps.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background on a list containing
        # """[
        #    'Background:',
        # ] """
        input_data = [
            'Background:',
        ]
        result = parser.section.get_background(input_data)

        # Then I see a background with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        self.assertEqual(
            result,
            {
                'background': {
                    'description': '',
                    'leading_comments_and_space': [],
                    'steps': [],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_background_with_description(self):
        """
            Check we can get background with description.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background on a list containing
        # """[
        #    'Background: Check',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            'Background: Check',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_background(input_data)

        # Then I see a background described as ' Check' with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        self.assertEqual(
            result,
            {
                'background': {
                    'description': ' Check',
                    'leading_comments_and_space': [],
                    'steps': [
                        {
                            'leading_comments_and_space': [],
                            'type': 'Given',
                            'text': 'a paperback book',
                            'multiline_arg': None,
                            'trailing_whitespace': [],
                        },
                        {
                            'leading_comments_and_space': [],
                            'type': 'When',
                            'text': 'I look at the back cover',
                            'multiline_arg': None,
                            'trailing_whitespace': [],
                        },
                        {
                            'leading_comments_and_space': [],
                            'type': 'Then',
                            'text': 'I see the blurb',
                            'multiline_arg': None,
                            'trailing_whitespace': [],
                        },
                    ],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_background_with_comment(self):
        """
            Check we can get background with comment.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background on a list containing
        # """[
        #    '# No comment',
        #    'Background:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            '# No comment',
            'Background:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_background(input_data)

        # Then I see a background with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # and leading comments and space of ['# No comment']
        self.assertEqual(
            result,
            {
                'background': {
                    'description': '',
                    'leading_comments_and_space': [
                        '# No comment',
                    ],
                    'steps': [
                        {
                            'leading_comments_and_space': [],
                            'type': 'Given',
                            'text': 'a paperback book',
                            'multiline_arg': None,
                            'trailing_whitespace': [],
                        },
                        {
                            'leading_comments_and_space': [],
                            'type': 'When',
                            'text': 'I look at the back cover',
                            'multiline_arg': None,
                            'trailing_whitespace': [],
                        },
                        {
                            'leading_comments_and_space': [],
                            'type': 'Then',
                            'text': 'I see the blurb',
                            'multiline_arg': None,
                            'trailing_whitespace': [],
                        },
                    ],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_background_with_trailing_space(self):
        """
            Check we can get a background with trailing space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background on a list containing
        # """[
        #    'Background:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        #    ' ',
        # ] """
        input_data = [
            'Background:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
            ' ',
        ]
        result = parser.section.get_background(input_data)

        # Then I see a background with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb',
        #   'trailing_whitespace': [' '] },
        # ]
        self.assertEqual(
            result,
            {
                'background': {
                    'description': '',
                    'leading_comments_and_space': [],
                    'steps': [
                        {
                            'leading_comments_and_space': [],
                            'type': 'Given',
                            'text': 'a paperback book',
                            'multiline_arg': None,
                            'trailing_whitespace': [],
                        },
                        {
                            'leading_comments_and_space': [],
                            'type': 'When',
                            'text': 'I look at the back cover',
                            'multiline_arg': None,
                            'trailing_whitespace': [],
                        },
                        {
                            'leading_comments_and_space': [],
                            'type': 'Then',
                            'text': 'I see the blurb',
                            'multiline_arg': None,
                            'trailing_whitespace': [
                                ' ',
                            ],
                        },
                    ],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_no_background_with_leading_noise(self):
        """
            Confirm we get no background with leading noise.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background on a list containing
        # """[
        #    'Noisy line',
        #    'Background:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            'Noisy line',
            'Background:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_background(input_data)

        # Then I see no background with remaining ['Noisy line',
        # 'Background:', 'Given a paperback book',
        # 'When I look at the back cover', 'Then I see the blurb']
        self.assertEqual(
            result,
            {
                'background': None,
                'remaining': [
                    'Noisy line',
                    'Background:',
                    'Given a paperback book',
                    'When I look at the back cover',
                    'Then I see the blurb',
                ],
                'raw_input': input_data,
            },
        )

    def test_background_with_trailing_background(self):
        """
            Check we can get only one background when there are two.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background on a list containing
        # """[
        #    'Background:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        #    'Background:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            'Background:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
            'Background:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_background(input_data)

        # Then I see a background with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # and remaining: ['Background:', 'Given a paperback book',
        # 'When I look at the back cover', 'Then I see the blurb']
        self.assertEqual(
            result,
            {
                'background': {
                    'description': '',
                    'leading_comments_and_space': [],
                    'steps': [
                        {
                            'leading_comments_and_space': [],
                            'type': 'Given',
                            'text': 'a paperback book',
                            'multiline_arg': None,
                            'trailing_whitespace': [],
                        },
                        {
                            'leading_comments_and_space': [],
                            'type': 'When',
                            'text': 'I look at the back cover',
                            'multiline_arg': None,
                            'trailing_whitespace': [],
                        },
                        {
                            'leading_comments_and_space': [],
                            'type': 'Then',
                            'text': 'I see the blurb',
                            'multiline_arg': None,
                            'trailing_whitespace': [],
                        },
                    ],
                },
                'remaining': [
                    'Background:',
                    'Given a paperback book',
                    'When I look at the back cover',
                    'Then I see the blurb',
                ],
                'raw_input': input_data,
            },
        )

    def test_no_background_with_no_input(self):
        """
            Confirm we get no background for no input.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background on an empty list
        result = parser.section.get_background([])

        # Then I see no background
        self.assertEqual(
            result,
            {
                'background': None,
                'remaining': [],
                'raw_input': [],
            },
        )
