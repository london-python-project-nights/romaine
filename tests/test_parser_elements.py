import unittest
from tests import common


class TestElementsParser(unittest.TestCase):
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

    def test_getting_elements_no_input_modification(self):
        """
            Test that getting elements doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_elements on a list containing
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
        parser.section.get_elements(input_var)

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

    def test_get_elements_one_scenario(self):
        """
            Check we can get one scenario.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_elements on a list containing
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
        result = parser.section.get_elements(input_data)

        # Then I see one scenario with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        self.assertEqual(
            result,
            {
                'elements': [
                    {
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
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_elements_one_outline(self):
        """
            Check we can get one scenario outline.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_elements on a list containing
        # """[
        #    'Scenario Outline:',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        # ] """
        input_data = [
            'Scenario Outline:',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
        ]
        result = parser.section.get_elements(input_data)

        # Then I see one scenario outline with steps: [
        # { 'type': 'Given', 'text': 'a <book> book' },
        # { 'type': 'When', 'text': 'I look at the <location>' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # with examples: [
        # { 'columns': { 'book': ['paperback'], 'location': ['back cover'] }}
        # ]
        self.assertEqual(
            result,
            {
                'elements': [
                    {
                        'type': 'scenario outline',
                        'tags': [],
                        'description': '',
                        'leading_comments_and_space': [],
                        'examples': [
                            {
                                'leading_comments_and_space': [],
                                'description': '',
                                'columns': {
                                    'book': [
                                        'paperback',
                                    ],
                                    'location': [
                                        'back cover',
                                    ],
                                },
                                'trailing_whitespace': [],
                            },
                        ],
                        'steps': [
                            {
                                'leading_comments_and_space': [],
                                'type': 'Given',
                                'text': 'a <book> book',
                                'multiline_arg': None,
                                'trailing_whitespace': [],
                            },
                            {
                                'leading_comments_and_space': [],
                                'type': 'When',
                                'text': 'I look at the <location>',
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
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_multiple_elements(self):
        """
            Check we can get more than one scenario/outline.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_elements on a list containing
        # """[
        #    'Scenario Outline:',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            'Scenario Outline:',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_elements(input_data)

        # Then I see one scenario outline with steps: [
        # { 'type': 'Given', 'text': 'a <book> book' },
        # { 'type': 'When', 'text': 'I look at the <location>' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # with examples: [
        # { 'columns': { 'book': ['paperback'], 'location': ['back cover'] }}
        # ]
        # followed by one scenario with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        self.assertEqual(
            result,
            {
                'elements': [
                    {
                        'type': 'scenario outline',
                        'tags': [],
                        'description': '',
                        'leading_comments_and_space': [],
                        'examples': [
                            {
                                'leading_comments_and_space': [],
                                'description': '',
                                'columns': {
                                    'book': [
                                        'paperback',
                                    ],
                                    'location': [
                                        'back cover',
                                    ],
                                },
                                'trailing_whitespace': [],
                            },
                        ],
                        'steps': [
                            {
                                'leading_comments_and_space': [],
                                'type': 'Given',
                                'text': 'a <book> book',
                                'multiline_arg': None,
                                'trailing_whitespace': [],
                            },
                            {
                                'leading_comments_and_space': [],
                                'type': 'When',
                                'text': 'I look at the <location>',
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
                    {
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
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_multiple_elements_trailing_noise(self):
        """
            Check we don't eat trailing noise with elements.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_elements on a list containing
        # """[
        #    'Scenario Outline:',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        #    'Missing this',
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
            'Scenario Outline:',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
            'Missing this',
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_elements(input_data)

        # Then I see one scenario with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # followed by one scenario outline with steps: [
        # { 'type': 'Given', 'text': 'a <book> book' },
        # { 'type': 'When', 'text': 'I look at the <location>' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # with examples: [
        # { 'columns': { 'book': ['paperback'], 'location': ['back cover'] }}
        # ]
        # with remaining: ['Missing this', 'Scenario:',
        # 'Given a paperback book', 'When I look at the back cover',
        # 'Then I see the blurb']
        self.assertEqual(
            result,
            {
                'elements': [
                    {
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
                    {
                        'type': 'scenario outline',
                        'tags': [],
                        'description': '',
                        'leading_comments_and_space': [],
                        'examples': [
                            {
                                'leading_comments_and_space': [],
                                'description': '',
                                'columns': {
                                    'book': [
                                        'paperback',
                                    ],
                                    'location': [
                                        'back cover',
                                    ],
                                },
                                'trailing_whitespace': [],
                            },
                        ],
                        'steps': [
                            {
                                'leading_comments_and_space': [],
                                'type': 'Given',
                                'text': 'a <book> book',
                                'multiline_arg': None,
                                'trailing_whitespace': [],
                            },
                            {
                                'leading_comments_and_space': [],
                                'type': 'When',
                                'text': 'I look at the <location>',
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
                ],
                'remaining': [
                    'Missing this',
                    'Scenario:',
                    'Given a paperback book',
                    'When I look at the back cover',
                    'Then I see the blurb',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_elements_one_scenario_with_leading_noise(self):
        """
            Check we cannot get one scenario with leading noise.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_elements on a list containing
        # """[
        #    'Leading noise',
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            'Leading noise',
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        result = parser.section.get_elements(input_data)

        # Then I see no elements, with remaining: ['Leading noise',
        # 'Scenario:', 'Given a paperback book',
        # 'When I look at the back cover', 'Then I see the blurb']
        self.assertEqual(
            result,
            {
                'elements': [],
                'remaining': [
                    'Leading noise',
                    'Scenario:',
                    'Given a paperback book',
                    'When I look at the back cover',
                    'Then I see the blurb',
                ],
                'raw_input': input_data,
            },
        )

    def test_get_no_elements_from_nothing(self):
        """
            Check we cannot get any elements from nothing.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_elements with an empty list
        results = parser.section.get_elements([])

        # Then I see no elements
        self.assertEqual(
            results,
            {
                'elements': [],
                'remaining': [],
                'raw_input': [],
            },
        )
