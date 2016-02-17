import unittest
from tests import common


class TestScenarioOutlinesParser(unittest.TestCase):
    """
        Test scenario outlines gherkin parser functionality of romaine's core.
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

    def test_getting_scenario_outline_no_input_modification(self):
        """
            Test that getting scenario outline doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Scenario Outline:',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        # ] """
        input_var = [
            'Scenario Outline:',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
        ]
        parser.section.get_element(input_var)

        # Then my input variable is not modified
        self.assertEqual(
            input_var,
            [
                'Scenario Outline:',
                'Given a <book> book',
                'When I look at the <location>',
                'Then I see the blurb',
                'Examples:',
                '|book|location|',
                '|paperback|back cover|',
            ],
        )

    def test_basic_scenario_outline(self):
        """
            Check we can get basic scenario outlines.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
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
        result = parser.section.get_element(input_data)

        # Then I see a scenario outline with steps: [
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
                'element': {
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
                            'table': [
                                ['book', 'location'],
                                ['paperback', 'back cover'],
                            ],
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
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_basic_scenario_outline_without_examples(self):
        """
            Check we can get basic scenario outlines without examples.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Scenario Outline:',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        # ] """
        input_data = [
            'Scenario Outline:',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
        ]
        result = parser.section.get_element(input_data)

        # Then I see a scenario outline with steps: [
        # { 'type': 'Given', 'text': 'a <book> book' },
        # { 'type': 'When', 'text': 'I look at the <location>' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        self.assertEqual(
            result,
            {
                'element': {
                    'type': 'scenario outline',
                    'tags': [],
                    'description': '',
                    'leading_comments_and_space': [],
                    'examples': [],
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
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_basic_scenario_outline_with_leading_comment(self):
        """
            Check we can get basic scenario outline with leading comment.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    '# Hello',
        #    '',
        #    'Scenario Outline:',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        # ] """
        input_data = [
            '# Hello',
            '',
            'Scenario Outline:',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
        ]
        result = parser.section.get_element(input_data)

        # Then I see a scenario outline with steps: [
        # { 'type': 'Given', 'text': 'a <book> book' },
        # { 'type': 'When', 'text': 'I look at the <location>' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # with examples: [
        # { 'columns': { 'book': ['paperback'], 'location': ['back cover'] }}
        # ]
        # and leading comments and space of ['# Hello', '']
        self.assertEqual(
            result,
            {
                'element': {
                    'type': 'scenario outline',
                    'tags': [],
                    'description': '',
                    'leading_comments_and_space': [
                        '# Hello',
                        '',
                    ],
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
                            'table': [
                                ['book', 'location'],
                                ['paperback', 'back cover'],
                            ],
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
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_basic_scenario_outline_with_trailing_space(self):
        """
            Check we can get basic scenario outline with trailing space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Scenario Outline:',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        #    '',
        # ] """
        input_data = [
            'Scenario Outline:',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
            '',
        ]
        result = parser.section.get_element(input_data)

        # Then I see a scenario outline with steps: [
        # { 'type': 'Given', 'text': 'a <book> book' },
        # { 'type': 'When', 'text': 'I look at the <location>' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # with examples: [
        # { 'columns': { 'book': ['paperback'], 'location': ['back cover'],
        #   'trailing_whitespace': [''] }}
        # ]
        self.assertEqual(
            result,
            {
                'element': {
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
                            'trailing_whitespace': [
                                '',
                            ],
                            'table': [
                                ['book', 'location'],
                                ['paperback', 'back cover'],
                            ],
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
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_basic_scenario_outline_leading_comment_and_trailing_space(self):
        """
            Check we can get scenario outline with comment and trailing space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    '# Hello',
        #    '',
        #    'Scenario Outline:',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        #    '',
        # ] """
        input_data = [
            '# Hello',
            '',
            'Scenario Outline:',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
            ''
        ]
        result = parser.section.get_element(input_data)

        # Then I see a scenario outline with steps: [
        # { 'type': 'Given', 'text': 'a <book> book' },
        # { 'type': 'When', 'text': 'I look at the <location>' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # with examples: [
        # { 'columns': { 'book': ['paperback'], 'location': ['back cover'],
        #   'trailing_whitespace': [''] }}
        # ]
        # and leading comments and space of ['# Hello', '']
        self.assertEqual(
            result,
            {
                'element': {
                    'type': 'scenario outline',
                    'tags': [],
                    'description': '',
                    'leading_comments_and_space': [
                        '# Hello',
                        '',
                    ],
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
                            'trailing_whitespace': [
                                '',
                            ],
                            'table': [
                                ['book', 'location'],
                                ['paperback', 'back cover'],
                            ],
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
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_basic_scenario_outline_no_steps(self):
        """
            Check we can get basic scenario outline without steps.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Scenario Outline:',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        # ] """
        input_data = [
            'Scenario Outline:',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
        ]
        result = parser.section.get_element(input_data)

        # Then I see a scenario outline with examples: [
        # { 'columns': { 'book': ['paperback'], 'location': ['back cover'] }}
        # ]
        self.assertEqual(
            result,
            {
                'element': {
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
                            'table': [
                                ['book', 'location'],
                                ['paperback', 'back cover'],
                            ],
                        },
                    ],
                    'steps': [],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_basic_scenario_outline_with_description(self):
        """
            Check we can get basic scenario outline with description.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Scenario Outline: Happy outline',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        # ] """
        input_data = [
            'Scenario Outline: Happy outline',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
        ]
        result = parser.section.get_element(input_data)

        # Then I see a scenario outline described as ' Happy outline'
        # with steps: [
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
                'element': {
                    'type': 'scenario outline',
                    'tags': [],
                    'description': ' Happy outline',
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
                            'table': [
                                ['book', 'location'],
                                ['paperback', 'back cover'],
                            ],
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
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_basic_scenario_outline_with_tags(self):
        """
            Check we can get basic scenario outline with tags.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    '@tagcloud',
        #    'Scenario Outline:',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        # ] """
        input_data = [
            '@tagcloud',
            'Scenario Outline:',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
        ]
        result = parser.section.get_element(input_data)

        # Then I see a scenario outline with steps: [
        # { 'type': 'Given', 'text': 'a <book> book' },
        # { 'type': 'When', 'text': 'I look at the <location>' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # with examples: [
        # { 'columns': { 'book': ['paperback'], 'location': ['back cover'] }}
        # ]
        # and tags: ['tagcloud']
        self.assertEqual(
            result,
            {
                'element': {
                    'type': 'scenario outline',
                    'tags': [
                        'tagcloud'
                    ],
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
                            'table': [
                                ['book', 'location'],
                                ['paperback', 'back cover'],
                            ],
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
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_basic_scenario_outline_with_tag_and_comment(self):
        """
            Check we can get basic scenario outline with tag and comment.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    '# Try this',
        #    '@trytag',
        #    'Scenario Outline:',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        # ] """
        input_data = [
            '# Try this',
            '@trytag',
            'Scenario Outline:',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
        ]
        result = parser.section.get_element(input_data)

        # Then I see a scenario outline with steps: [
        # { 'type': 'Given', 'text': 'a <book> book' },
        # { 'type': 'When', 'text': 'I look at the <location>' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # with examples: [
        # { 'columns': { 'book': ['paperback'], 'location': ['back cover'] }}
        # ]
        # and leading comments and space of ['# Try this']
        # and tags: ['trytag']
        self.assertEqual(
            result,
            {
                'element': {
                    'type': 'scenario outline',
                    'tags': [
                        'trytag',
                    ],
                    'description': '',
                    'leading_comments_and_space': [
                        '# Try this',
                    ],
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
                            'table': [
                                ['book', 'location'],
                                ['paperback', 'back cover'],
                            ],
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
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_basic_scenario_outline_with_trailing_outline(self):
        """
            Check we can get basic scenario outline without second outline.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Scenario Outline:',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        #    'Scenario Outline:',
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
            'Scenario Outline:',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
        ]
        result = parser.section.get_element(input_data)

        # Then I see a scenario outline with steps: [
        # { 'type': 'Given', 'text': 'a <book> book' },
        # { 'type': 'When', 'text': 'I look at the <location>' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # with examples: [
        # { 'columns': { 'book': ['paperback'], 'location': ['back cover'] }}
        # ]
        # and remaining: [ 'Scenario Outline:', 'Given a <book> book',
        # 'When I look at the <location>', 'Then I see the blurb',
        # 'Examples:', '|book|location|', '|paperback|back cover|' ]
        self.assertEqual(
            result,
            {
                'element': {
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
                            'table': [
                                ['book', 'location'],
                                ['paperback', 'back cover'],
                            ],
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
                'remaining': [
                    'Scenario Outline:',
                    'Given a <book> book',
                    'When I look at the <location>',
                    'Then I see the blurb',
                    'Examples:',
                    '|book|location|',
                    '|paperback|back cover|',
                ],
                'raw_input': input_data,
            },
        )

    def test_do_not_get_scenario_outline_with_leading_noise(self):
        """
            Confirm we get no outline with leading noise.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Ignore me',
        #    'Scenario Outline:',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        # ] """
        input_data = [
            'Ignore me',
            'Scenario Outline:',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
        ]
        result = parser.section.get_element(input_data)

        # Then I see no scenario outline with remaining: [ 'Ignore me',
        # 'Scenario Outline:', 'Given a <book> book',
        # 'When I look at the <location>', 'Then I see the blurb',
        # 'Examples:', '|book|location|', '|paperback|back cover|' ]
        self.assertEqual(
            result,
            {
                'element': None,
                'remaining': [
                    'Ignore me',
                    'Scenario Outline:',
                    'Given a <book> book',
                    'When I look at the <location>',
                    'Then I see the blurb',
                    'Examples:',
                    '|book|location|',
                    '|paperback|back cover|',
                ],
                'raw_input': input_data,
            },
        )

    def test_scenario_outline_with_two_examples(self):
        """
            Check we can get scenario outline with two examples sections.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element on a list containing
        # """[
        #    'Scenario Outline:',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        #    'Examples:',
        #    '|book|location|',
        #    '|hardback|inside of the front cover|',
        # ] """
        input_data = [
            'Scenario Outline:',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
            'Examples:',
            '|book|location|',
            '|hardback|inside of the front cover|',
        ]
        result = parser.section.get_element(input_data)

        # Then I see a scenario outline with steps: [
        # { 'type': 'Given', 'text': 'a <book> book' },
        # { 'type': 'When', 'text': 'I look at the <location>' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        # with examples: [
        # { 'columns': { 'book': ['paperback'], 'location': ['back cover'] }}
        # { 'columns': { 'book': ['hardback'],
        #   'location': ['inside of the front cover'] }}
        # ]
        self.assertEqual(
            result,
            {
                'element': {
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
                            'table': [
                                ['book', 'location'],
                                ['paperback', 'back cover'],
                            ],
                        },
                        {
                            'leading_comments_and_space': [],
                            'description': '',
                            'columns': {
                                'book': [
                                    'hardback',
                                ],
                                'location': [
                                    'inside of the front cover',
                                ],
                            },
                            'trailing_whitespace': [],
                            'table': [
                                ['book', 'location'],
                                ['hardback', 'inside of the front cover'],
                            ],
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
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_do_not_get_scenario_from_nothing(self):
        """
            Confirm we get no outline with no input.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with an empty list
        result = parser.section.get_element([])

        # Then I see no scenario outline
        self.assertEqual(
            result,
            {
                'element': None,
                'remaining': [],
                'raw_input': [],
            },
        )
