from copy import deepcopy
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

    def test_getting_background_no_input_modification(self):
        """
            Test that getting scenario doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background with input from background/basic_input
        input_data = common.get_parser_input('background/basic_input')

        expected_data = deepcopy(input_data)

        parser.section.get_background(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )

    def test_basic_background(self):
        """
            Check we can get basic backgrounds.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background with input from background/basic_input
        input_data = common.get_parser_input('background/basic_input')

        result = parser.section.get_background(input_data)

        # Then I see the results from background/basic_expected
        self.assertEqual(
            result,
            common.get_parser_output('background/basic_expected'),
        )

    def test_background_without_steps(self):
        """
            Check we can get a background without steps.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background with input from background/no_steps_input
        input_data = common.get_parser_input('background/no_steps_input')

        result = parser.section.get_background(input_data)

        # Then I see the results from background/no_steps_expected
        self.assertEqual(
            result,
            common.get_parser_output('background/no_steps_expected'),
        )

    def test_background_with_description(self):
        """
            Check we can get background with description.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background with input from
        # background/with_description_input
        input_data = common.get_parser_input(
            'background/with_description_input',
        )

        result = parser.section.get_background(input_data)

        # Then I see the results from background/with_description_expected
        self.assertEqual(
            result,
            common.get_parser_output('background/with_description_expected'),
        )

    def test_background_with_comment(self):
        """
            Check we can get background with comment.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background with input from
        # background/with_comment_input
        input_data = common.get_parser_input('background/with_comment_input')

        result = parser.section.get_background(input_data)

        # Then I see the results from background/with_comment_expected
        self.assertEqual(
            result,
            common.get_parser_output('background/with_comment_expected'),
        )

    def test_background_with_trailing_space(self):
        """
            Check we can get a background with trailing space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background with input from
        # background/with_trailing_space_input
        input_data = common.get_parser_input(
            'background/with_trailing_space_input',
        )

        result = parser.section.get_background(input_data)

        # Then I see the results from background/with_trailing_space_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'background/with_trailing_space_expected',
            ),
        )

    def test_no_background_with_leading_noise(self):
        """
            Confirm we get no background with leading noise.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background with input from
        # background/with_leading_noise_input
        input_data = common.get_parser_input(
            'background/with_leading_noise_input',
        )

        result = parser.section.get_background(input_data)

        # Then I see the results from background/with_leading_noise_input
        self.assertEqual(
            result,
            common.get_parser_output(
                'background/with_leading_noise_expected',
            ),
        )

    def test_background_with_trailing_background(self):
        """
            Check we can get only one background when there are two.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background with input from
        # background/with_trailing_background_input
        input_data = common.get_parser_input(
            'background/with_trailing_background_input',
        )

        result = parser.section.get_background(input_data)

        # Then I see the results from
        # background/with_trailing_background_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'background/with_trailing_background_expected',
            ),
        )

    def test_no_background_with_no_input(self):
        """
            Confirm we get no background for no input.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_background with input from background/no_input
        input_data = common.get_parser_input('background/no_input')

        result = parser.section.get_background(input_data)

        # Then I see no background
        self.assertEqual(
            result,
            common.get_parser_output('background/no_input_expected'),
        )
