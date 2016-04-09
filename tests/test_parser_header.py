from copy import deepcopy
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

    def test_getting_header_no_input_modification(self):
        """
            Test that getting header doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_header with input from header/basic_input
        input_data = common.get_parser_input('header/basic_input')

        expected_data = deepcopy(input_data)

        parser.section.get_header(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )

    def test_just_header(self):
        """
            Check we can get a header alone.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_header with input from header/basic_input
        input_data = common.get_parser_input('header/basic_input')

        result = parser.section.get_header(input_data)

        # Then I see the results from header/basic_expected
        self.assertEqual(
            result,
            common.get_parser_output('header/basic_expected'),
        )

    def test_header_with_scenario_and_noise(self):
        """
            Check we can get a header without eating the following scenario.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_header with input from header/with_scenario_input
        input_data = common.get_parser_input('header/with_scenario_input')

        result = parser.section.get_header(input_data)

        # Then I see the results from header/with_scenario_expected
        self.assertEqual(
            result,
            common.get_parser_output('header/with_scenario_expected'),
        )

    def test_header_with_scenario_outline_and_noise(self):
        """
            Check we can get a header without eating the following outline.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_header with input from
        # header/with_scenario_outline_input
        input_data = common.get_parser_input(
            'header/with_scenario_outline_input',
        )

        result = parser.section.get_header(input_data)

        # Then I see the results from header/with_scenario_outline_expected
        self.assertEqual(
            result,
            common.get_parser_output('header/with_scenario_outline_expected'),
        )

    def test_header_with_background_and_noise(self):
        """
            Check we can get a header without eating the following background.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_header with input from
        # header/with_background_input
        input_data = common.get_parser_input(
            'header/with_background_input',
        )

        result = parser.section.get_header(input_data)

        # Then I see the results from header/with_background_expected
        self.assertEqual(
            result,
            common.get_parser_output('header/with_background_expected'),
        )

    def test_no_header_from_nothing(self):
        """
            Confirm we get no header from no input.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_header with input from header/empty_input
        input_data = common.get_parser_input(
            'header/empty_input',
        )

        result = parser.section.get_header(input_data)

        # Then I see the results from header/empty_expected
        self.assertEqual(
            result,
            common.get_parser_output('header/empty_expected'),
        )
