from copy import deepcopy
import unittest
from tests import common

from romaine.parser.exceptions import (
    MalformedTableError,
)


class TestExamplesParser(unittest.TestCase):
    """
        Test examples gherkin parser functionality of romaine's core.
    """
    def setUp(self):
        """
            Prepare the environment for testing.
        """
        # We're doing a lot of long tests- don't limit the diff output length
        self.maxDiff = None

    def test_getting_example_no_input_modification(self):
        """
            Test that getting example doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example with input from examples/basic_input
        input_data = common.get_parser_input('examples/basic_input')

        expected_data = deepcopy(input_data)

        parser.section.get_example(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )

    def test_basic_examples_without_description(self):
        """
            Check we can get examples with no description.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example with input from examples/basic_input
        input_data = common.get_parser_input('examples/basic_input')

        result = parser.section.get_example(input_data)

        # Then I see the results from examples/basic_expected
        self.assertEqual(
            result,
            common.get_parser_output('examples/basic_expected'),
        )

    def test_basic_examples_with_description(self):
        """
            Check description can be extracted from an example when present.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example with input from examples/description_input
        input_data = common.get_parser_input('examples/description_input')

        result = parser.section.get_example(input_data)

        # Then I see the results from examples/description_expected
        self.assertEqual(
            result,
            common.get_parser_output('examples/description_expected'),
        )

    def test_malformed_examples_table_causes_exception(self):
        """
            Check that a malformed table throws an exception.
        """

        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example with input from
        # examples/malformed_examples_table_input
        input_data = common.get_parser_input(
            'examples/malformed_examples_table_input',
        )
        # Then I see a MalformedTableError
        with self.assertRaises(MalformedTableError):
            parser.section.get_example(input_data)

    def test_examples_with_incomplete_table(self):
        """
            Confirm we can retrieve example with just table headings.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example with input from
        # examples/incomplete_table_input
        input_data = common.get_parser_input(
            'examples/incomplete_table_input',
        )

        result = parser.section.get_example(input_data)

        # Then I see the results from
        # examples/incomplete_table_expected
        self.assertEqual(
            result,
            common.get_parser_output('examples/incomplete_table_expected'),
        )

    def test_examples_with_leading_comment_and_whitespace_can_be_parsed(self):
        """
            Check that examples with leading comment and whitespace are valid.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example with input from
        # examples/comment_and_whitespace_input
        input_data = common.get_parser_input(
            'examples/comment_and_whitespace_input',
        )

        result = parser.section.get_example(input_data)

        # Then I see the results from
        # examples/comment_and_whitespace_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'examples/comment_and_whitespace_expected',
            ),
        )

    def test_example_with_trailing_data_and_whitespace(self):
        """
            Check that examples with trailing whitespace and data are valid.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example with input from
        # examples/trailing_data_and_whitespace_input
        input_data = common.get_parser_input(
            'examples/trailing_data_and_whitespace_input',
        )

        result = parser.section.get_example(input_data)

        # Then I see the results from
        # examples/trailing_data_and_whitespace_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'examples/trailing_data_and_whitespace_expected',
            ),
        )

    def test_multiple_examples_sections(self):
        """
            Check that a second example will be left alone.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example with input from
        # examples/one_from_multiple_examples_input
        input_data = common.get_parser_input(
            'examples/one_from_multiple_examples_input',
        )

        result = parser.section.get_example(input_data)

        # Then I see the results from
        # examples/one_from_multiple_examples_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'examples/one_from_multiple_examples_expected',
            ),
        )

    def test_no_examples_sections_with_trailing_data(self):
        """
            Check that no examples sections returns no examples.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example with input from
        # examples/no_examples_input
        input_data = common.get_parser_input(
            'examples/no_examples_input',
        )

        result = parser.section.get_example(input_data)

        # Then I see the results from
        # examples/no_examples_expected
        self.assertEqual(
            result,
            common.get_parser_output('examples/no_examples_expected'),
        )

    def test_no_examples_from_nothing(self):
        """
            Check that we don't crash trying to get examples from nothing.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example with input from
        # examples/empty_input
        input_data = common.get_parser_input(
            'examples/empty_input',
        )

        result = parser.section.get_example(input_data)

        # Then I see the results from
        # examples/empty_expected
        self.assertEqual(
            result,
            common.get_parser_output('examples/empty_expected'),
        )

    def test_examples_divorced_from_table(self):
        """
            Confirm we don't get examples when the table is not attached.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example with input from
        # examples/missing_table_input
        input_data = common.get_parser_input(
            'examples/missing_table_input',
        )

        result = parser.section.get_example(input_data)

        # Then I see the results from
        # examples/missing_table_expected
        self.assertEqual(
            result,
            common.get_parser_output('examples/missing_table_expected'),
        )

    def test_basic_single_examples_without_description(self):
        """
            Check we can get a single example with no description.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example with input from
        # examples/single_example_input
        input_data = common.get_parser_input(
            'examples/single_example_input',
        )

        result = parser.section.get_examples(input_data)

        # Then I see the results from
        # examples/single_example_expected
        self.assertEqual(
            result,
            common.get_parser_output('examples/single_example_expected'),
        )

    def test_get_multiple_examples_sections(self):
        """
            Check that we can retrieve two examples sections.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example with input from
        # examples/multiple_examples_input
        input_data = common.get_parser_input(
            'examples/multiple_examples_input',
        )

        result = parser.section.get_examples(input_data)

        # Then I see the results from
        # examples/multiple_examples_expected
        self.assertEqual(
            result,
            common.get_parser_output('examples/multiple_examples_expected'),
        )

    def test_get_one_example_with_example_following_other_data(self):
        """
            Check that an example not immediately following is left alone.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_example with input from
        # examples/noise_between_examples_input
        input_data = common.get_parser_input(
            'examples/noise_between_examples_input',
        )

        result = parser.section.get_examples(input_data)

        # Then I see the results from
        # examples/noise_between_examples_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'examples/noise_between_examples_expected',
            ),
        )

    def test_do_not_get_multiple_examples_from_nothing(self):
        """
            Check that we can't get many (any) examples from nothing.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_examples with input from
        # examples/empty_input
        input_data = common.get_parser_input(
            'examples/empty_input',
        )

        result = parser.section.get_examples(input_data)

        # Then I see the results from
        # examples/empty_examples_expected
        self.assertEqual(
            result,
            common.get_parser_output('examples/empty_examples_expected'),
        )

    def test_get_examples_no_input_modification(self):
        """
            Test that getting examples doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_examples with input from examples/basic_input
        input_data = common.get_parser_input('examples/basic_input')

        expected_data = deepcopy(input_data)

        parser.section.get_examples(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )
