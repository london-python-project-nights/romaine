import unittest
from tests import common

from romaine.parser.exceptions import FeatureTrailingDataError


class TestFeatureParser(unittest.TestCase):
    """
        Test feature gherkin parser functionality of romaine's core.
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

    def test_getting_feature_no_input_modification(self):
        """
            Test that getting feature doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_feature on a list containing
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
        parser.feature.get_feature(input_var)

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

    def test_get_feature(self):
        """
            Check we can get a feature.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_feature on a list containing
        # """[
        #    '@smtp',
        #    '@base',
        #    'Feature: Basic SMTP server',
        #    '  In order to successfully use an SMTP server it must listen '
        #    'on port 25.',
        #    '  If it does not do this then most SMTP servers will have '
        #    'difficulty',
        #    '  delivering mail to this server.',
        #    '',
        #    '  @expected_port',
        #    '  Scenario: Check the server is listening on tcp/25',
        #    '     Given I have an SMTP server',
        #    '      When I attempt to connect to port 25',
        #    '      Then I am connected to port 25',
        #    '',
        #    '  @relay_test',
        #    '  Scenario: Check the server will not relay unauthenticated '
        #    'traffic',
        #    '     Given I have an SMTP server',
        #    '      When I attempt to deliver mail to '
        #    'nobody@example.notrelayed',
        #    '      Then The server responds with a status of 554 for '
        #    'nobody@example.notrelayed',
        #    '',
        #    '  @valid_destination_test',
        #    '  @valid_recipient',
        #    '  Scenario: Check the server will accept mail to itself',
        #    '     Given I have an SMTP server',
        #    '      When I attempt to deliver mail to the current user',
        #    '      Then The server responds with a status of 250 for the '
        #    'current user',
        # ] """
        input_data = [
            '@smtp',
            '@base',
            'Feature: Basic SMTP server',
            '  In order to successfully use an SMTP server it must listen '
            'on port 25.',
            '  If it does not do this then most SMTP servers will have '
            'difficulty',
            '  delivering mail to this server.',
            '',
            '  @expected_port',
            '  Scenario: Check the server is listening on tcp/25',
            '     Given I have an SMTP server',
            '      When I attempt to connect to port 25',
            '      Then I am connected to port 25',
            '',
            '  @relay_test',
            '  Scenario: Check the server will not relay unauthenticated '
            'traffic',
            '     Given I have an SMTP server',
            '      When I attempt to deliver mail to '
            'nobody@example.notrelayed',
            '      Then The server responds with a status of 554 for '
            'nobody@example.notrelayed',
            '',
            '  @valid_destination_test',
            '  @valid_recipient',
            '  Scenario: Check the server will accept mail to itself',
            '     Given I have an SMTP server',
            '      When I attempt to deliver mail to the current user',
            '      Then The server responds with a status of 250 for the '
            'current user',
        ]
        result = parser.feature.get_feature(input_data)

        # Then I see an scenario with steps: [
        # { 'type': 'Given', 'text': 'a paperback book' },
        # { 'type': 'When', 'text': 'I look at the back cover' },
        # { 'type': 'Then', 'text': 'I see the blurb' },
        # ]
        self.assertEqual(
            result,
            {
                'feature': {
                    'header': [
                        'Feature: Basic SMTP server',
                        '  In order to successfully use an SMTP server it '
                        'must listen on port 25.',
                        '  If it does not do this then most SMTP servers '
                        'will have difficulty',
                        '  delivering mail to this server.',
                        '',
                    ],
                    'tags': [
                        'smtp',
                        'base',
                    ],
                    'background': None,
                    'leading_space_and_comments': [],
                    'trailing_space_and_comments': [],
                    'elements': [
                        {
                            'type': 'scenario',
                            'tags': [
                                'expected_port'
                            ],
                            'description': (
                                ' Check the server is listening on tcp/25'
                            ),
                            'leading_comments_and_space': [],
                            'steps': [
                                {
                                    'leading_comments_and_space': [],
                                    'type': 'Given',
                                    'text': 'I have an SMTP server',
                                    'multiline_arg': None,
                                    'trailing_whitespace': [],
                                },
                                {
                                    'leading_comments_and_space': [],
                                    'type': 'When',
                                    'text': 'I attempt to connect to port 25',
                                    'multiline_arg': None,
                                    'trailing_whitespace': [],
                                },
                                {
                                    'leading_comments_and_space': [],
                                    'type': 'Then',
                                    'text': 'I am connected to port 25',
                                    'multiline_arg': None,
                                    'trailing_whitespace': [
                                        '',
                                    ],
                                },
                            ],
                        },
                        {
                            'type': 'scenario',
                            'tags': [
                                'relay_test'
                            ],
                            'description': (
                                ' Check the server will not relay '
                                'unauthenticated traffic'
                            ),
                            'leading_comments_and_space': [],
                            'steps': [
                                {
                                    'leading_comments_and_space': [],
                                    'type': 'Given',
                                    'text': 'I have an SMTP server',
                                    'multiline_arg': None,
                                    'trailing_whitespace': [],
                                },
                                {
                                    'leading_comments_and_space': [],
                                    'type': 'When',
                                    'text': (
                                        'I attempt to deliver mail to '
                                        'nobody@example.notrelayed'
                                    ),
                                    'multiline_arg': None,
                                    'trailing_whitespace': [],
                                },
                                {
                                    'leading_comments_and_space': [],
                                    'type': 'Then',
                                    'text': (
                                        'The server responds with a status of'
                                        ' 554 for nobody@example.notrelayed'
                                    ),
                                    'multiline_arg': None,
                                    'trailing_whitespace': [
                                        '',
                                    ],
                                },
                            ],
                        },
                        {
                            'type': 'scenario',
                            'tags': [
                                'valid_destination_test',
                                'valid_recipient',
                            ],
                            'description': (
                                ' Check the server will accept mail to '
                                'itself'
                            ),
                            'leading_comments_and_space': [],
                            'steps': [
                                {
                                    'leading_comments_and_space': [],
                                    'type': 'Given',
                                    'text': 'I have an SMTP server',
                                    'multiline_arg': None,
                                    'trailing_whitespace': [],
                                },
                                {
                                    'leading_comments_and_space': [],
                                    'type': 'When',
                                    'text': (
                                        'I attempt to deliver mail to the '
                                        'current user'
                                    ),
                                    'multiline_arg': None,
                                    'trailing_whitespace': [],
                                },
                                {
                                    'leading_comments_and_space': [],
                                    'type': 'Then',
                                    'text': (
                                        'The server responds with a status of'
                                        ' 250 for the current user'
                                    ),
                                    'multiline_arg': None,
                                    'trailing_whitespace': [],
                                },
                            ],
                        },
                    ],
                },
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_get_no_feature_trailing_noise(self):
        """
            Confirm exception raised when we don't end in something parseable.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_feature on a list containing:
        # """[
        #    'Feature: Test a features',
        #    'Scenario: Some scenario',
        #    'Given a cake',
        #    'When I break this',
        #    'Then I do something',
        #    "This won't work.",
        # ] """
        # Then I see a FeatureTrailingDataError
        with self.assertRaises(FeatureTrailingDataError):
            input_data = [
                'Feature: Test a features',
                'Scenario: Some scenario',
                'Given a cake',
                'When I break this',
                'Then I do something',
                "This won't work.",
            ]
            parser.feature.get_feature(input_data)
