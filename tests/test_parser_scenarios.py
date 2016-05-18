from copy import deepcopy
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

    def test_getting_scenario_no_input_modification(self):
        """
            Test that getting scenario doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with input from scenario/basic_input
        input_data = common.get_parser_input('scenario/basic_input')

        expected_data = deepcopy(input_data)

        parser.section.get_element(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )

    def test_basic_scenario(self):
        """
            Check we can get basic scenarios.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with input from scenario/basic_input
        input_data = common.get_parser_input('scenario/basic_input')

        result = parser.section.get_element(input_data)

        # Then I see the results from scenario/basic_expected
        self.assertEqual(
            result,
            common.get_parser_output('scenario/basic_expected'),
        )

    def test_basic_scenario_with_leading_comments_and_space(self):
        """
            Check we can get scenarios with leading comments and space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with input from
        # scenario/leading_comments_and_space_input
        input_data = common.get_parser_input(
            'scenario/leading_comments_and_space_input',
        )

        result = parser.section.get_element(input_data)

        # Then I see the results from
        # scenario/leading_comments_and_space_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'scenario/leading_comments_and_space_expected',
            ),
        )

    def test_basic_scenario_with_trailing_space(self):
        """
            Check we can get basic scenarios with trailing whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with input from
        # scenario/trailing_space_input
        input_data = common.get_parser_input(
            'scenario/trailing_space_input',
        )

        result = parser.section.get_element(input_data)

        # Then I see the results from
        # scenario/trailing_space_expected
        self.assertEqual(
            result,
            common.get_parser_output('scenario/trailing_space_expected'),
        )

    def test_basic_scenario_with_leading_comment_and_trailing_space(self):
        """
            Check we can get basic scenarios with comment and trailing space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with input from
        # scenario/leading_and_trailing_space_and_comment_input
        input_data = common.get_parser_input(
            'scenario/leading_and_trailing_space_and_comment_input',
        )

        result = parser.section.get_element(input_data)

        # Then I see the results from
        # scenario/leading_and_trailing_space_and_comment_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'scenario/leading_and_trailing_space_and_comment_expected',
            ),
        )

    def test_basic_scenario_with_no_steps(self):
        """
            Confirm we can get a scenario with no steps.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with input from
        # scenario/no_steps_input
        input_data = common.get_parser_input(
            'scenario/no_steps_input',
        )

        result = parser.section.get_element(input_data)

        # Then I see the results from
        # scenario/no_steps_expected
        self.assertEqual(
            result,
            common.get_parser_output('scenario/no_steps_expected'),
        )

    def test_get_scenario_with_description(self):
        """
            Check we can get a scenario with a description.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with input from
        # scenario/description_input
        input_data = common.get_parser_input(
            'scenario/description_input',
        )

        result = parser.section.get_element(input_data)

        # Then I see the results from
        # scenario/description_expected
        self.assertEqual(
            result,
            common.get_parser_output('scenario/description_expected'),
        )

    def test_get_scenario_with_tags(self):
        """
            Check we can get a scenario with tags.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with input from
        # scenario/tags_input
        input_data = common.get_parser_input(
            'scenario/tags_input',
        )

        result = parser.section.get_element(input_data)

        # Then I see the results from
        # scenario/tags_expected
        self.assertEqual(
            result,
            common.get_parser_output('scenario/tags_expected'),
        )

    def test_get_scenario_with_tags_and_comments(self):
        """
            Check we can get a scenario with tags and comments.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with input from
        # scenario/tags_and_comments_input
        input_data = common.get_parser_input(
            'scenario/tags_and_comments_input',
        )

        result = parser.section.get_element(input_data)

        # Then I see the results from
        # scenario/tags_and_comments_expected
        self.assertEqual(
            result,
            common.get_parser_output('scenario/tags_and_comments_expected'),
        )

    def test_two_scenarios_in_a_row(self):
        """
            Check we get only the first scenario from input.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with input from
        # scenario/two_scenarios_input
        input_data = common.get_parser_input(
            'scenario/two_scenarios_input',
        )

        result = parser.section.get_element(input_data)

        # Then I see the results from
        # scenario/two_scenarios_expected
        self.assertEqual(
            result,
            common.get_parser_output('scenario/two_scenarios_expected'),
        )

    def test_fail_to_get_scenario_with_leading_noise(self):
        """
            Confirm we don't get a scenario if there is noise before it.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with input from
        # scenario/leading_noise_input
        input_data = common.get_parser_input(
            'scenario/leading_noise_input',
        )

        result = parser.section.get_element(input_data)

        # Then I see the results from
        # scenario/leading_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output('scenario/leading_noise_expected'),
        )

    def test_get_scenario_no_input(self):
        """
            Confirm we don't get a scenario if there is empty input.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with input from
        # scenario/empty_input
        input_data = common.get_parser_input(
            'scenario/empty_input',
        )

        result = parser.section.get_element(input_data)

        # Then I see the results from
        # scenario/empty_expected
        self.assertEqual(
            result,
            common.get_parser_output('scenario/empty_expected'),
        )

    def test_get_no_scenario_with_leading_tags_and_comments(self):
        """
            Confirm we don't eat any lines when we don't get a scenario.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_element with input from
        # scenario/leading_tags_and_comments_then_noise_input
        input_data = common.get_parser_input(
            'scenario/leading_tags_and_comments_then_noise_input',
        )

        result = parser.section.get_element(input_data)

        # Then I see the results from
        # scenario/leading_tags_and_comments_then_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'scenario/leading_tags_and_comments_then_noise_expected',
            ),
        )
