import unittest
from tests import common


class TestHeaderParser(unittest.TestCase):
    """
        Test header gherkin parser functionality of romaine's core.
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

    def test_getting_header_no_input_modification(self):
        """
            Test that getting header doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_header on a list containing
        # """[
        #    'This is a header',
        #    'It heads the feature nicely',
        #    'If the code works well',
        #    '',
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        # ] """
        input_var = [
            'This is a header',
            'It heads the feature nicely',
            'If the code works well',
            '',
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
        ]
        parser.section.get_header(input_var)

        # Then my input variable is not modified
        self.assertEqual(
            input_var,
            [
                'This is a header',
                'It heads the feature nicely',
                'If the code works well',
                '',
                'Scenario:',
                'Given a paperback book',
                'When I look at the back cover',
                'Then I see the blurb',
            ],
        )

    def test_just_header(self):
        """
            Check we can get a header alone.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_header on a list containing
        # """[
        #    'This is a header',
        #    'It heads the feature nicely',
        #    'If the code works well',
        # ] """
        input_data = [
            'This is a header',
            'It heads the feature nicely',
            'If the code works well',
        ]
        result = parser.section.get_header(input_data)

        # Then I see a header: ['This is a header',
        # 'It heads the feature nicely', 'If the code works well']
        self.assertEqual(
            result,
            {
                'header': [
                    'This is a header',
                    'It heads the feature nicely',
                    'If the code works well',
                ],
                'remaining': [],
                'raw_input': input_data,
            },
        )

    def test_header_with_scenario_and_noise(self):
        """
            Check we can get a header without eating the following scenario.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_header on a list containing
        # """[
        #    'This is a header',
        #    'It heads the feature nicely',
        #    'If the code works well',
        #    '',
        #    'Scenario:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        #    'More stuff',
        # ] """
        input_data = [
            'This is a header',
            'It heads the feature nicely',
            'If the code works well',
            '',
            'Scenario:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
            'More stuff',
        ]
        result = parser.section.get_header(input_data)

        # Then I see a header: ['This is a header',
        # 'It heads the feature nicely', 'If the code works well']
        # and remaining: ['Scenario:', 'Given a paperback book',
        # 'When I look at the back cover', 'Then I see the blurb',
        # 'More stuff']
        self.assertEqual(
            result,
            {
                'header': [
                    'This is a header',
                    'It heads the feature nicely',
                    'If the code works well',
                    '',
                ],
                'remaining': [
                    'Scenario:',
                    'Given a paperback book',
                    'When I look at the back cover',
                    'Then I see the blurb',
                    'More stuff',
                ],
                'raw_input': input_data,
            },
        )

    def test_header_with_scenario_outline_and_noise(self):
        """
            Check we can get a header without eating the following outline.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_header on a list containing
        # """[
        #    'This is a header',
        #    'It heads the feature nicely',
        #    'If the code works well',
        #    '',
        #    'Scenario Outline:',
        #    'Given a <book> book',
        #    'When I look at the <location>',
        #    'Then I see the blurb',
        #    'Examples:',
        #    '|book|location|',
        #    '|paperback|back cover|',
        #    'More stuff',
        # ] """
        input_data = [
            'This is a header',
            'It heads the feature nicely',
            'If the code works well',
            '',
            'Scenario Outline:',
            'Given a <book> book',
            'When I look at the <location>',
            'Then I see the blurb',
            'Examples:',
            '|book|location|',
            '|paperback|back cover|',
            'More stuff',
        ]
        result = parser.section.get_header(input_data)

        # Then I see a header: ['This is a header',
        # 'It heads the feature nicely', 'If the code works well']
        # and remaining: ['Scenario Outline:', 'Given a <book> book',
        # 'When I look at the <location>', 'Then I see the blurb',
        # 'Examples:', '|book|location|', '|paperback|back cover|',
        # 'More stuff']
        self.assertEqual(
            result,
            {
                'header': [
                    'This is a header',
                    'It heads the feature nicely',
                    'If the code works well',
                    '',
                ],
                'remaining': [
                    'Scenario Outline:',
                    'Given a <book> book',
                    'When I look at the <location>',
                    'Then I see the blurb',
                    'Examples:',
                    '|book|location|',
                    '|paperback|back cover|',
                    'More stuff',
                ],
                'raw_input': input_data,
            },
        )

    def test_header_with_background_and_noise(self):
        """
            Check we can get a header without eating the following background.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_header on a list containing
        # """[
        #    'This is a header',
        #    'It heads the feature nicely',
        #    'If the code works well',
        #    '',
        #    'Background:',
        #    'Given a paperback book',
        #    'When I look at the back cover',
        #    'Then I see the blurb',
        #    'More stuff',
        # ] """
        input_data = [
            'This is a header',
            'It heads the feature nicely',
            'If the code works well',
            '',
            'Background:',
            'Given a paperback book',
            'When I look at the back cover',
            'Then I see the blurb',
            'More stuff',
        ]
        result = parser.section.get_header(input_data)

        # Then I see a header: ['This is a header',
        # 'It heads the feature nicely', 'If the code works well']
        # and remaining: ['Background:', 'Given a paperback book',
        # 'When I look at the back cover', 'Then I see the blurb',
        # 'More stuff']
        self.assertEqual(
            result,
            {
                'header': [
                    'This is a header',
                    'It heads the feature nicely',
                    'If the code works well',
                    '',
                ],
                'remaining': [
                    'Background:',
                    'Given a paperback book',
                    'When I look at the back cover',
                    'Then I see the blurb',
                    'More stuff',
                ],
                'raw_input': input_data,
            },
        )

    def test_no_header_from_nothing(self):
        """
            Confirm we get no header from no input.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_header with an empty list
        result = parser.section.get_header([])

        # Then I see no header
        self.assertEqual(
            result,
            {
                'header': [],
                'remaining': [],
                'raw_input': [],
            },
        )
