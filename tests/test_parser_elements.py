from copy import deepcopy
import unittest
from tests import common


class TestElementsParser(unittest.TestCase):
    """
        Test elements gherkin parser functionality of romaine's core.
    """
    def setUp(self):
        """
            Prepare the environment for testing.
        """
        # We're doing a lot of long tests- don't limit the diff output length
        self.maxDiff = None

    def test_getting_elements_no_input_modification(self):
        """
            Test that getting elements doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_elements with input from
        # elements/one_scenario_input
        input_data = common.get_parser_input(
            'elements/one_scenario_input',
        )

        expected_data = deepcopy(input_data)

        parser.section.get_elements(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )

    def test_get_elements_one_scenario(self):
        """
            Check we can get one scenario.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_elements with input from
        # elements/one_scenario_input
        input_data = common.get_parser_input(
            'elements/one_scenario_input',
        )

        result = parser.section.get_elements(input_data)

        # Then I see the results from
        # elements/one_scenario_expected
        self.assertEqual(
            result,
            common.get_parser_output('elements/one_scenario_expected'),
        )

    def test_get_elements_one_outline(self):
        """
            Check we can get one scenario outline.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_elements with input from
        # elements/one_outline_input
        input_data = common.get_parser_input(
            'elements/one_outline_input',
        )

        result = parser.section.get_elements(input_data)

        # Then I see the results from
        # elements/one_outline_expected
        self.assertEqual(
            result,
            common.get_parser_output('elements/one_outline_expected'),
        )

    def test_get_multiple_elements(self):
        """
            Check we can get more than one scenario/outline.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_elements with input from
        # elements/multiple_elements_input
        input_data = common.get_parser_input(
            'elements/multiple_elements_input',
        )

        result = parser.section.get_elements(input_data)

        # Then I see the results from
        # elements/multiple_elements_expected
        self.assertEqual(
            result,
            common.get_parser_output('elements/multiple_elements_expected'),
        )

    def test_get_multiple_elements_trailing_noise(self):
        """
            Check we don't eat trailing noise with elements.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_elements with input from
        # elements/multiple_elements_trailing_noise_input
        input_data = common.get_parser_input(
            'elements/multiple_elements_trailing_noise_input',
        )

        result = parser.section.get_elements(input_data)

        # Then I see the results from
        # elements/multiple_elements_trailing_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'elements/multiple_elements_trailing_noise_expected',
            ),
        )

    def test_get_elements_one_scenario_with_empty(self):
        """
            Check we cannot get one scenario with leading noise.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_elements with input from
        # elements/empty_input
        input_data = common.get_parser_input(
            'elements/empty_input',
        )

        result = parser.section.get_elements(input_data)

        # Then I see the results from
        # elements/empty_expected
        self.assertEqual(
            result,
            common.get_parser_output('elements/empty_expected'),
        )

    def test_get_no_elements_from_nothing(self):
        """
            Check we cannot get any elements from nothing.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_elements with input from
        # elements/empty_input
        input_data = common.get_parser_input(
            'elements/empty_input',
        )

        result = parser.section.get_elements(input_data)

        # Then I see the results from
        # elements/empty_expected
        self.assertEqual(
            result,
            common.get_parser_output('elements/empty_expected'),
        )
