from copy import deepcopy
import unittest
from tests import common


class TestStepsParser(unittest.TestCase):
    """
        Test steps gherkin parser functionality of romaine's core.
    """
    def setUp(self):
        """
            Prepare the environment for testing.
        """
        # We're doing a lot of long tests- don't limit the diff output length
        self.maxDiff = None

    def test_getting_step_no_input_modification(self):
        """
            Test that getting a step doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step with input from step/basic_input
        input_data = common.get_parser_input('step/basic_input')

        expected_data = deepcopy(input_data)

        parser.step.get_step(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )

    def test_getting_raw_step(self):
        """
            Check we can get a step with no surrounding data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step with input from step/basic_input
        input_data = common.get_parser_input('step/basic_input')

        result = parser.step.get_step(input_data)

        # Then I see the results from step/basic_expected
        self.assertEqual(
            result,
            common.get_parser_output('step/basic_expected'),
        )

    def test_getting_commented_step(self):
        """
            Check we can get a step with a leading comment.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step with input from step/commented_input
        input_data = common.get_parser_input('step/commented_input')

        result = parser.step.get_step(input_data)

        # Then I see the results from step/commented_expected
        self.assertEqual(
            result,
            common.get_parser_output('step/commented_expected'),
        )

    def test_get_step_leading_noise(self):
        """
            Confirm that we get nothing when we don't start with a step.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step with input from step/leading_noise_input
        input_data = common.get_parser_input('step/leading_noise_input')

        result = parser.step.get_step(input_data)

        # Then I see the results from step/leading_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output('step/leading_noise_expected'),
        )

    def test_get_step_with_table(self):
        """
            Confirm that we can get a step with a table.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step with input from step/with_table_input
        input_data = common.get_parser_input('step/with_table_input')

        result = parser.step.get_step(input_data)

        # Then I see the results from step/with_table_expected
        self.assertEqual(
            result,
            common.get_parser_output('step/with_table_expected'),
        )

    def test_get_step_with_pythonish_string(self):
        """
            Confirm that we can get a step with a pythonish string.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step with input from step/with_string_input
        input_data = common.get_parser_input('step/with_string_input')

        result = parser.step.get_step(input_data)

        # Then I see the results from step/with_string_expected
        self.assertEqual(
            result,
            common.get_parser_output('step/with_string_expected'),
        )

    def test_get_step_with_divorced_multiline_arg(self):
        """
            Confirm get step with no multiline arg, separated by whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step with input from
        # step/with_space_then_string_input
        input_data = common.get_parser_input(
            'step/with_space_then_string_input'
        )

        result = parser.step.get_step(input_data)

        # Then I see the results from step/with_space_then_string_expected
        self.assertEqual(
            result,
            common.get_parser_output('step/with_space_then_string_expected'),
        )

    def test_get_step_with_multiline_arg_and_trailing_whitespace(self):
        """
            Confirm we get a step with multiline arg and trailing whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step with input from
        # step/multiline_arg_trailing_space_input
        input_data = common.get_parser_input(
            'step/multiline_arg_trailing_space_input'
        )

        result = parser.step.get_step(input_data)

        # Then I see the results from
        # step/multiline_arg_trailing_space_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'step/multiline_arg_trailing_space_expected',
            ),
        )

    def test_get_step_with_trailing_step(self):
        """
            Confirm we get a step with multiline arg and trailing whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step with input from
        # step/trailing_step_input
        input_data = common.get_parser_input(
            'step/trailing_step_input'
        )

        result = parser.step.get_step(input_data)

        # Then I see the results from
        # step/trailing_step_expected
        self.assertEqual(
            result,
            common.get_parser_output('step/trailing_step_expected'),
        )

    def test_get_no_step_from_no_lines(self):
        """
            Confirm that we get no step from no lines.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_step with input from
        # step/empty_input
        input_data = common.get_parser_input(
            'step/empty_input'
        )

        result = parser.step.get_step(input_data)

        # Then I see the results from
        # step/empty_expected
        self.assertEqual(
            result,
            common.get_parser_output('step/empty_expected'),
        )

    def test_getting_steps_no_input_modification(self):
        """
            Test that getting steps doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_steps with input from steps/leading_noise_input
        input_data = common.get_parser_input('steps/leading_noise_input')

        expected_data = deepcopy(input_data)

        parser.step.get_steps(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )

    def test_fail_to_get_steps(self):
        """
            Confirm we get no steps with leading noise.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_steps with input from
        # steps/leading_noise_input
        input_data = common.get_parser_input(
            'steps/leading_noise_input'
        )

        result = parser.step.get_steps(input_data)

        # Then I see the results from
        # steps/leading_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output('steps/leading_noise_expected'),
        )

    def test_get_steps_single_step(self):
        """
            Confirm we can get a single step when getting steps.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_steps with input from
        # steps/one_step_input
        input_data = common.get_parser_input(
            'steps/one_step_input'
        )

        result = parser.step.get_steps(input_data)

        # Then I see the results from
        # steps/one_step_expected
        self.assertEqual(
            result,
            common.get_parser_output('steps/one_step_expected'),
        )

    def test_get_two_steps(self):
        """
            Confirm we can get two steps.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_steps with input from
        # steps/two_steps_input
        input_data = common.get_parser_input(
            'steps/two_steps_input'
        )

        result = parser.step.get_steps(input_data)

        # Then I see the results from
        # steps/two_steps_expected
        self.assertEqual(
            result,
            common.get_parser_output('steps/two_steps_expected'),
        )

    def test_get_no_steps_from_no_lines(self):
        """
            Confirm that we get no steps from no lines.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_steps with input from
        # step/empty_input
        input_data = common.get_parser_input(
            'steps/empty_input'
        )

        result = parser.step.get_steps(input_data)

        # Then I see the results from
        # steps/empty_expected
        self.assertEqual(
            result,
            common.get_parser_output('steps/empty_expected'),
        )
