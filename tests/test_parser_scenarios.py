import unittest
from tests import common


class TestScenariosParser(unittest.TestCase):
    """
        Test scenarios gherkin parser functionality of romaine's core.
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

    def test_getting_scenario_no_input_modification(self):
        """
            Test that getting scenario doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_var = [
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        parser.section.get_element(input_var)

        # Then my input variable is not modified
        self.assertEqual(
            input_var,
            [
                'Scenario:',
                'Given a paperback book',
                'When I look at the back cover',
                'Then I see the blurb',
            ],
        )

    def test_basic_scenario(self):
        """
            Check we can get basic scenarios.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_element(input_data)

        # Then I see an scenario with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        self.assertEqual(
            result,
            {
                'element': {
                    'type': 'scenario',
                    'tags': [],
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

    def test_basic_scenario_with_leading_comments_and_space(self):
        """
            Check we can get scenarios with leading comments and space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    '# Helpful comment',
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            '# Helpful comment',
            '',
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_element(input_data)

        # Then I see an scenario with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # and leading comments and space of: ['# Helpful comment', '']
        self.assertEqual(
            result,
            {
                'element': {
                    'type': 'scenario',
                    'tags': [],
                    'description': '',
                    'leading_comments_and_space': [
                        '# Helpful comment',
                        '',
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

    def test_basic_scenario_with_trailing_space(self):
        """
            Check we can get basic scenarios with trailing whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        #    '',
        #    '  \t ',
        # ] """
        input_data = [
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
            '',
            '  \t ',
        ]
        result = parser.section.get_element(input_data)

        # Then I see an scenario with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb',
        #   'trailing_whitespace': ['', '  \t '] },
        # ]
        self.assertEqual(
            result,
            {
                'element': {
                    'type': 'scenario',
                    'tags': [],
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
                                '',
                                '  \t ',
                            ],
                        },
                    ],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_basic_scenario_with_leading_comment_and_trailing_space(self):
        """
            Check we can get basic scenarios with comment and trailing space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    '# Helpful comment',
        #    '',
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        #    '',
        #    '  \t ',
        # ] """
        input_data = [
            '# Helpful comment',
            '',
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
            '',
            '  \t ',
        ]
        result = parser.section.get_element(input_data)

        # Then I see an scenario with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb',
        #   'trailing_whitespace': ['', '  \t '] },
        # ]
        # and leading comments and space of: ['# Helpful comment', '']
        self.assertEqual(
            result,
            {
                'element': {
                    'type': 'scenario',
                    'tags': [],
                    'description': '',
                    'leading_comments_and_space': [
                        '# Helpful comment',
                        '',
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
                            'trailing_whitespace': [
                                '',
                                '  \t ',
                            ],
                        },
                    ],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_basic_scenario_with_no_steps(self):
        """
            Confirm we can get a scenario with no steps.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Scenario:',
        # ] """
        input_data = [
            'Scenario:',
        ]
        result = parser.section.get_element(input_data)

        # Then I see a scenario with no description and no steps
        self.assertEqual(
            result,
            {
                'element': {
                    'type': 'scenario',
                    'tags': [],
                    'description': '',
                    'leading_comments_and_space': [],
                    'steps': [],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_scenario_with_description(self):
        """
            Check we can get a scenario with a description.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Scenario: This is my scenario',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            'Scenario: This is my scenario',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_element(input_data)

        # Then I see an scenario described as 'This is my scenario'
        # with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        self.assertEqual(
            result,
            {
                'element': {
                    'type': 'scenario',
                    'tags': [],
                    'description': ' This is my scenario',
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

    def test_get_scenario_with_tags(self):
        """
            Check we can get a scenario with tags.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    '@by_the_book',
        #    '@new_test_library',
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            '@by_the_book',
            '@new_test_library',
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_element(input_data)

        # Then I see an scenario with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        self.assertEqual(
            result,
            {
                'element': {
                    'type': 'scenario',
                    'tags': [
                        'by_the_book',
                        'new_test_library',
                    ],
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

    def test_get_scenario_with_tags_and_comments(self):
        """
            Check we can get a scenario with tags and comments.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    '# This test needs more pictures',
        #    '@by_the_book',
        #    '@new_test_library',
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            '# Test needs more pictures',
            '@by_the_book',
            '@new_test_library',
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_element(input_data)

        # Then I see an scenario with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # and leading comments and space of: ['# Test needs more pictures']
        self.assertEqual(
            result,
            {
                'element': {
                    'type': 'scenario',
                    'tags': [
                        'by_the_book',
                        'new_test_library',
                    ],
                    'description': '',
                    'leading_comments_and_space': [
                        '# Test needs more pictures',
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

    def test_two_scenarios_in_a_row(self):
        """
            Check we get only the first scenario from input.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        #    'Scenario:',
        #    'Given a hardback book',
        #    'When I look inside the front cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
            'Scenario:',
            'Given a hardback book',
            'When I look inside the front cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_element(input_data)

        # Then I see an scenario with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # and remaining: ['Scenario:', 'Given a hardback book',
        # 'When I look inside the front cover', 'Then I see the blurb']
        self.assertEqual(
            result,
            {
                'element': {
                    'type': 'scenario',
                    'tags': [],
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
                    'Scenario:',
                    'Given a hardback book',
                    'When I look inside the front cover',
                    'Then I see the blurb',
                ],
                'raw_input': input_data,
            },
        )

    def test_fail_to_get_scenario_with_leading_noise(self):
        """
            Confirm we don't get a scenario if there is noise before it.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Broken',
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            'Broken',
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_element(input_data)

        # Then I see no scenario, and remaining: ['Broken', 'Scenario:',
        # 'Given a paperback book', 'When I look at the back cover',
        # 'Then I see the blurb']
        self.assertEqual(
            result,
            {
                'element': None,
                'remaining': [
                    'Broken',
                    'Scenario:',
                    'Given a paperback book',
                    'When I look at the back cover',
                    'Then I see the blurb',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_scenario_no_input(self):
        """
            Confirm we don't get a scenario if there is empty input.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with an empty list
        result = parser.section.get_element([])

        # Then I see no scenario
        self.assertEqual(
            result,
            {
                'element': None,
                'remaining': [],
                'raw_input': [],
            },
        )

    def test_get_no_scenario_with_leading_tags_and_comments(self):
        """
            Confirm we don't eat any lines when we don't get a scenario.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    '# Do not eat this',
        #    '@not_for_algorithmic_consumption',
        #    'Broken',
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            '# Do not eat this',
            '@not_for_algorithmic_consumption',
            'Broken',
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_element(input_data)

        # Then I see no scenario, and remaining: ['# Do not eat this',
        # '@not_for_algorithmic_consumption', 'Broken', 'Scenario:',
        # 'Given a paperback book', 'When I look at the back cover',
        # 'Then I see the blurb']
        self.assertEqual(
            result,
            {
                'element': None,
                'remaining': [
                    '# Do not eat this',
                    '@not_for_algorithmic_consumption',
                    'Broken',
                    'Scenario:',
                    'Given a paperback book',
                    'When I look at the back cover',
                    'Then I see the blurb',
                ],
                'raw_input': input_data,
            },
        )
