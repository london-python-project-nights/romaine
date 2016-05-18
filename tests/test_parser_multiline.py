from copy import deepcopy
import unittest
from tests import common

from romaine.parser.exceptions import UnclosedPythonishString


class TestMultilineParser(unittest.TestCase):
    """
        Test multi-line gherkin parser functionality of romaine's core.
    """
    def setUp(self):
        """
            Prepare the environment for testing.
        """
        # We're doing a lot of long tests- don't limit the diff output length
        self.maxDiff = None

    def test_getting_pythonish_string_no_input_modification(self):
        """
            Test that getting a pythonish string doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string with input from
        # multiline/pythonish_string_input
        input_data = common.get_parser_input(
            'multiline/pythonish_string_input',
        )

        expected_data = deepcopy(input_data)

        parser.multiline.get_pythonish_string(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )

    def test_getting_pythonish_string(self):
        """
            Check we can get a pythonish string.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string with input from
        # multiline/pythonish_string_input
        input_data = common.get_parser_input(
            'multiline/pythonish_string_input',
        )

        result = parser.multiline.get_pythonish_string(input_data)

        # Then I see the results from multiline/pythonish_string_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/pythonish_string_expected'),
        )

    def test_getting_pythonish_string_with_delimiter_noise(self):
        """
            Check we can get a pythonish string with noise by the delimiters
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string with input from
        # multiline/pythonish_string_noisy_delimiters_input
        input_data = common.get_parser_input(
            'multiline/pythonish_string_noisy_delimiters_input',
        )

        result = parser.multiline.get_pythonish_string(input_data)

        # Then I see the results from
        # multiline/pythonish_string_noisy_delimiters_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/pythonish_string_noisy_delimiters_expected',
            ),
        )

    def test_getting_pythonish_string_with_trailing_data(self):
        """
            Check we can get a pythonish string with noise by the delimiters
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string with input from
        # multiline/pythonish_string_trailing_data_input
        input_data = common.get_parser_input(
            'multiline/pythonish_string_trailing_data_input',
        )

        result = parser.multiline.get_pythonish_string(input_data)

        # Then I see the results from
        # multiline/pythonish_string_trailing_data_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/pythonish_string_trailing_data_expected',
            ),
        )

    def test_fail_getting_single_quoted_pythonish_string(self):
        """
            Check we do not get a pythonish string with '''.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string with input from
        # multiline/pythonish_string_wrong_delimiter_input
        input_data = common.get_parser_input(
            'multiline/pythonish_string_wrong_delimiter_input',
        )

        result = parser.multiline.get_pythonish_string(input_data)

        # Then I see the results from
        # multiline/pythonish_string_wrong_delimiter_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/pythonish_string_wrong_delimiter_expected',
            ),
        )

    def test_fail_getting_not_following_pythonish_string(self):
        """
            Check we do not get a pythonish string with a leading line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string with input from
        # multiline/pythonish_string_leading_noise_input
        input_data = common.get_parser_input(
            'multiline/pythonish_string_leading_noise_input',
        )

        result = parser.multiline.get_pythonish_string(input_data)

        # Then I see the results from
        # multiline/pythonish_string_leading_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/pythonish_string_leading_noise_expected',
            ),
        )

    def test_fail_getting_unclosed_pythonish_string(self):
        """
            Check we fail noisily on an unclosed pythonish string.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string with input from
        # multiline/pythonish_string_unclosed_input
        input_data = common.get_parser_input(
            'multiline/pythonish_string_unclosed_input',
        )
        # Then an UnclosedPythonishString exception is raised
        with self.assertRaises(UnclosedPythonishString):
            parser.multiline.get_pythonish_string(input_data)

    def test_fail_getting_last_line_opening_pythonish_string(self):
        """
            Check we fail noisily when last line is opening python string.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string with input from
        # multiline/pythonish_string_unclosed_input
        input_data = common.get_parser_input(
            'multiline/pythonish_string_just_opening_input',
        )
        # Then an UnclosedPythonishString exception is raised
        with self.assertRaises(UnclosedPythonishString):
            parser.multiline.get_pythonish_string(input_data)

    def test_getting_table_no_input_modification(self):
        """
            Test that getting a table doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_table with input from
        # multiline/table_input
        input_data = common.get_parser_input(
            'multiline/table_input',
        )

        expected_data = deepcopy(input_data)

        parser.multiline.get_table(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )

    def test_get_one_row_one_cell_table(self):
        """
            Test that we can get a table consisting of one row with one cell.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_table with input from
        # multiline/table_input
        input_data = common.get_parser_input(
            'multiline/table_input',
        )

        result = parser.multiline.get_table(input_data)

        # Then I see the results from
        # multiline/table_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/table_expected'),
        )

    def test_get_one_row_multi_cell_table(self):
        """
            Test that we can get a table consisting of one row with two cells.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_table with input from
        # multiline/table_multi_column_input
        input_data = common.get_parser_input(
            'multiline/table_multi_column_input',
        )

        result = parser.multiline.get_table(input_data)

        # Then I see the results from
        # multiline/table_multi_column_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/table_multi_column_expected'),
        )

    def test_get_multi_row_multi_cell_table(self):
        """
            Test that we can get a table consisting of multiple rows.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_table with input from
        # multiline/table_multi_column_multi_row_input
        input_data = common.get_parser_input(
            'multiline/table_multi_column_multi_row_input',
        )

        result = parser.multiline.get_table(input_data)

        # Then I see the results from
        # multiline/table_multi_column_multi_row_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/table_multi_column_multi_row_expected',
            ),
        )

    def test_get_table_with_trailing_data(self):
        """
            Test that we can get a table consisting of multiple rows.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_table with input from
        # multiline/table_trailing_data_input
        input_data = common.get_parser_input(
            'multiline/table_trailing_data_input',
        )

        result = parser.multiline.get_table(input_data)

        # Then I see the results from
        # multiline/table_trailing_data_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/table_trailing_data_expected',
            ),
        )

    def test_fail_to_get_table(self):
        """
            Confirm we cannot get a table when we do not start with a row.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_table with input from
        # multiline/table_leading_noise_input
        input_data = common.get_parser_input(
            'multiline/table_leading_noise_input',
        )

        result = parser.multiline.get_table(input_data)

        # Then I see the results from
        # multiline/table_leading_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/table_leading_noise_expected',
            ),
        )

    def test_getting_multiline_arg_no_input_modification(self):
        """
            Test that getting a multiline arg doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_multiline_arg with input from
        # multiline/multiline_table_input
        input_data = common.get_parser_input(
            'multiline/multiline_table_input',
        )

        expected_data = deepcopy(input_data)

        parser.multiline.get_multiline_arg(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )

    def test_get_multiline_arg_table(self):
        """
            Check we can get a table as a multiline arg.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_multiline_arg with input from
        # multiline/multiline_table_input
        input_data = common.get_parser_input(
            'multiline/multiline_table_input',
        )

        result = parser.multiline.get_multiline_arg(input_data)

        # Then I see the results from
        # multiline/multiline_table_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/multiline_table_expected'),
        )

    def test_get_multiline_arg_pythonish_string(self):
        """
            Check we can get a pythonish string as a multiline arg.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_multiline_arg with input from
        # multiline/multiline_string_input
        input_data = common.get_parser_input(
            'multiline/multiline_string_input',
        )

        result = parser.multiline.get_multiline_arg(input_data)

        # Then I see the results from
        # multiline/multiline_string_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/multiline_string_expected'),
        )

    def test_get_no_multiline_arg(self):
        """
            Confirm we get nothing when no multiline arg is following.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_multiline_arg with input from
        # multiline/multiline_leading_noise_input
        input_data = common.get_parser_input(
            'multiline/multiline_leading_noise_input',
        )

        result = parser.multiline.get_multiline_arg(input_data)

        # Then I see the results from
        # multiline/multiline_leading_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/multiline_leading_noise_expected',
            ),
        )

    def test_getting_leading_comment_no_input_modification(self):
        """
            Test that getting leading comments doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/comments_space_basic_input
        input_data = common.get_parser_input(
            'multiline/comment_space_basic_input',
        )

        expected_data = deepcopy(input_data)

        parser.multiline.get_comments_with_space(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )

    def test_get_leading_comment_with_blank_line(self):
        """
            Check we can get a leading comment with following blank line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/comment_space_basic_input
        input_data = common.get_parser_input(
            'multiline/comment_space_basic_input',
        )

        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the results from
        # multiline/comment_space_basic_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/comment_space_basic_expected',
            ),
        )

    def test_get_leading_comment_without_space(self):
        """
            Check we can get a leading comment with no following whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/comment_space_just_comment_input
        input_data = common.get_parser_input(
            'multiline/comment_space_just_comment_input',
        )

        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the results from
        # multiline/comment_space_just_comment_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/comment_space_just_comment_expected',
            ),
        )

    def test_get_leading_comment_with_trailing_data(self):
        """
            Check we can get a leading comment with trailing data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/comment_space_trailing_data_input
        input_data = common.get_parser_input(
            'multiline/comment_space_trailing_data_input',
        )

        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the results from
        # multiline/comment_space_trailing_data_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/comment_space_trailing_data_expected',
            ),
        )

    def test_get_leading_comment_with_whitespace(self):
        """
            Check we can get a leading comment with following whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/comment_space_trailing_whitespace_input
        input_data = common.get_parser_input(
            'multiline/comment_space_trailing_whitespace_input',
        )

        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the results from
        # multiline/comment_space_trailing_whitespace_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/comment_space_trailing_whitespace_expected',
            ),
        )

    def test_get_leading_comment_with_whitespace_and_trailing_data(self):
        """
            Check we can get a leading comment with following space and data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/comment_space_whitespace_trailing_data_input
        input_data = common.get_parser_input(
            'multiline/comment_space_whitespace_trailing_data_input',
        )

        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the results from
        # multiline/comment_space_whitespace_trailing_data_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/comment_space_whitespace_trailing_data_expected',
            ),
        )

    def test_get_leading_comments(self):
        """
            Check we can get multiple leading comments.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/comment_space_multiple_comments_input
        input_data = common.get_parser_input(
            'multiline/comment_space_multiple_comments_input',
        )

        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the results from
        # multiline/comment_space_multiple_comments_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/comment_space_multiple_comments_expected',
            ),
        )

    def test_get_comments_with_space_and_trailing_data(self):
        """
            Check we can get leading comments and space with trailing data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/comment_space_comments_space_noise_input
        input_data = common.get_parser_input(
            'multiline/comment_space_comments_space_noise_input',
        )

        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the results from
        # multiline/comment_space_comments_space_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/comment_space_comments_space_noise_expected',
            ),
        )

    def test_get_leading_comments_with_multiple_trailing_lines(self):
        """
            Check we can get leading comments with multiple trailing lines.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/comment_space_comments_more_noise_input
        input_data = common.get_parser_input(
            'multiline/comment_space_comments_more_noise_input',
        )

        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the results from
        # multiline/comment_space_comments_more_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/comment_space_comments_more_noise_expected',
            ),
        )

    def test_get_leading_comments_space_separated_with_trailing_data(self):
        """
            Check we can get leading comments and spaces, and trailing data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/comment_space_intervening_space_input
        input_data = common.get_parser_input(
            'multiline/comment_space_intervening_space_input',
        )

        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the results from
        # multiline/comment_space_intervening_space_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/comment_space_intervening_space_expected',
            ),
        )

    def test_get_no_leading_comments_with_leading_space(self):
        """
            Confirm we cannot get a leading comment preceded by a blank line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/comment_space_leading_space_input
        input_data = common.get_parser_input(
            'multiline/comment_space_leading_space_input',
        )

        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the results from
        # multiline/comment_space_leading_space_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/comment_space_leading_space_expected',
            ),
        )

    def test_get_no_leading_comments_with_leading_noise(self):
        """
            Confirm we cannot get a leading comment preceded data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/comment_space_leading_noise_input
        input_data = common.get_parser_input(
            'multiline/comment_space_leading_noise_input',
        )

        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the results from
        # multiline/comment_space_leading_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/comment_space_leading_noise_expected',
            ),
        )

    def test_get_no_leading_comments_from_no_lines(self):
        """
            Confirm we cannot get a leading comment from nothing.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/comment_space_empty_input
        input_data = common.get_parser_input(
            'multiline/comment_space_empty_input',
        )

        result = parser.multiline.get_comments_with_space(input_data)

        # Then I see the results from
        # multiline/comment_space_empty_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/comment_space_empty_expected',
            ),
        )

    def test_getting_space_no_input_modification(self):
        """
            Test that getting space doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_pythonish_string with input from
        # multiline/pythonish_string_input
        input_data = common.get_parser_input(
            'multiline/space_no_space_input',
        )

        expected_data = deepcopy(input_data)

        parser.multiline.get_space(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )

    def test_get_space_non_whitespace(self):
        """
            Confirm that we get no whitespace from a non space line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/space_no_space_input
        input_data = common.get_parser_input(
            'multiline/space_no_space_input',
        )

        result = parser.multiline.get_space(input_data)

        # Then I see the results from
        # multiline/space_no_space_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/space_no_space_expected'),
        )

    def test_get_space_non_whitespace_then_space(self):
        """
            Confirm that we get no whitespace from a starting non space line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/space_leading_noise_input
        input_data = common.get_parser_input(
            'multiline/space_leading_noise_input',
        )

        result = parser.multiline.get_space(input_data)

        # Then I see the results from
        # multiline/space_leading_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/space_leading_noise_expected',
            ),
        )

    def test_get_space_blank_line(self):
        """
            Confirm that we get a blank line as space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/space_basic_input
        input_data = common.get_parser_input(
            'multiline/space_basic_input',
        )

        result = parser.multiline.get_space(input_data)

        # Then I see the results from
        # multiline/space_basic_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/space_basic_expected'),
        )

    def test_get_space_whitespace_line(self):
        """
            Confirm that we get a whitespace line as space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/space_whitespace_input
        input_data = common.get_parser_input(
            'multiline/space_whitespace_input',
        )

        result = parser.multiline.get_space(input_data)

        # Then I see the results from
        # multiline/space_whitespace_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/space_whitespace_expected'),
        )

    def test_get_space_whitespace_and_blank_line(self):
        """
            Confirm that we get a whitespace and blank line as space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/space_whitespace_and_blank_input
        input_data = common.get_parser_input(
            'multiline/space_whitespace_and_blank_input',
        )

        result = parser.multiline.get_space(input_data)

        # Then I see the results from
        # multiline/space_whitespace_and_blank_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/space_whitespace_and_blank_expected',
            ),
        )

    def test_get_space_followed_by_non_space(self):
        """
            Confirm that we get space with remaining non space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/space_whitespace_trailing_noise_input
        input_data = common.get_parser_input(
            'multiline/space_whitespace_trailing_noise_input',
        )

        result = parser.multiline.get_space(input_data)

        # Then I see the results from
        # multiline/space_whitespace_trailing_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/space_whitespace_trailing_noise_expected',
            ),
        )

    def test_get_space_nothing(self):
        """
            Confirm that we get no space from nothing.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/space_empty_input
        input_data = common.get_parser_input(
            'multiline/space_empty_input',
        )

        result = parser.multiline.get_space(input_data)

        # Then I see the results from
        # multiline/space_empty_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/space_empty_expected'),
        )

    def test_getting_leading_tag_no_input_modification(self):
        """
            Test that getting leading tags doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tag with input from
        # multiline/tag_trailing_blank_line_input
        input_data = common.get_parser_input(
            'multiline/tag_trailing_blank_line_input',
        )

        expected_data = deepcopy(input_data)

        parser.multiline.get_tags(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )

    def test_get_leading_tag_with_blank_line(self):
        """
            Check we can get a leading tag with following blank line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/tag_trailing_blank_line_input
        input_data = common.get_parser_input(
            'multiline/tag_trailing_blank_line_input',
        )

        result = parser.multiline.get_tags(input_data)

        # Then I see the results from
        # multiline/tag_trailing_blank_line_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/tag_trailing_blank_line_expected',
            ),
        )

    def test_get_leading_tag_without_space(self):
        """
            Check we can get a leading tag with no following whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/tag_basic_input
        input_data = common.get_parser_input(
            'multiline/tag_basic_input',
        )

        result = parser.multiline.get_tags(input_data)

        # Then I see the results from
        # multiline/tag_basic_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/tag_basic_expected'),
        )

    def test_get_leading_tag_with_trailing_data(self):
        """
            Check we can get a leading tag with trailing data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/tag_trailing_data_input
        input_data = common.get_parser_input(
            'multiline/tag_trailing_data_input',
        )

        result = parser.multiline.get_tags(input_data)

        # Then I see the results from
        # multiline/tag_trailing_data_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/tag_trailing_data_expected'),
        )

    def test_get_leading_tag_with_whitespace(self):
        """
            Check we can get a leading tag with following whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/tag_trailing_space_input
        input_data = common.get_parser_input(
            'multiline/tag_trailing_space_input',
        )

        result = parser.multiline.get_tags(input_data)

        # Then I see the results from
        # multiline/tag_trailing_space_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/tag_trailing_space_expected'),
        )

    def test_get_leading_tag_with_whitespace_and_trailing_data(self):
        """
            Check we can get a leading tag with following space and data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/tag_trailing_space_and_noise_input
        input_data = common.get_parser_input(
            'multiline/tag_trailing_space_and_noise_input',
        )

        result = parser.multiline.get_tags(input_data)

        # Then I see the results from
        # multiline/tag_trailing_space_and_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/tag_trailing_space_and_noise_expected',
            ),
        )

    def test_get_leading_tags(self):
        """
            Check we can get multiple leading tags.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/tag_multiple_tags_input
        input_data = common.get_parser_input(
            'multiline/tag_multiple_tags_input',
        )

        result = parser.multiline.get_tags(input_data)

        # Then I see the results from
        # multiline/tag_multiple_tags_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/tag_multiple_tags_expected'),
        )

    def test_get_tags_and_trailing_data(self):
        """
            Check we can get leading tags and space with trailing data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/tag_multiple_tags_trailing_noise_input
        input_data = common.get_parser_input(
            'multiline/tag_multiple_tags_trailing_noise_input',
        )

        result = parser.multiline.get_tags(input_data)

        # Then I see the results from
        # multiline/tag_multiple_tags_trailing_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/tag_multiple_tags_trailing_noise_expected',
            ),
        )

    def test_get_leading_tags_with_multiple_trailing_lines(self):
        """
            Check we can get leading tags with multiple trailing lines.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/tag_longer_trailing_noise_input
        input_data = common.get_parser_input(
            'multiline/tag_longer_trailing_noise_input',
        )

        result = parser.multiline.get_tags(input_data)

        # Then I see the results from
        # multiline/tag_longer_trailing_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/tag_longer_trailing_noise_expected',
            ),
        )

    def test_get_leading_tags_space_separated_with_trailing_data(self):
        """
            Check we can get leading tags and spaces, and trailing data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/tag_tags_with_space_trailing_noise_input
        input_data = common.get_parser_input(
            'multiline/tag_tags_with_space_trailing_noise_input',
        )

        result = parser.multiline.get_tags(input_data)

        # Then I see the results from
        # multiline/tag_tags_with_space_trailing_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output(
                'multiline/tag_tags_with_space_trailing_noise_expected',
            ),
        )

    def test_get_no_leading_tags_with_leading_space(self):
        """
            Confirm we cannot get a leading tag preceded by a blank line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/tag_leading_space_input
        input_data = common.get_parser_input(
            'multiline/tag_leading_space_input',
        )

        result = parser.multiline.get_tags(input_data)

        # Then I see the results from
        # multiline/tag_leading_space_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/tag_leading_space_expected'),
        )

    def test_get_no_leading_tags_with_leading_noise(self):
        """
            Confirm we cannot get a leading tag preceded data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/tag_leading_noise_input
        input_data = common.get_parser_input(
            'multiline/tag_leading_noise_input',
        )

        result = parser.multiline.get_tags(input_data)

        # Then I see the results from
        # multiline/tag_leading_noise_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/tag_leading_noise_expected'),
        )

    def test_get_no_leading_tags_from_no_lines(self):
        """
            Confirm we cannot get a leading tag from nothing.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_comments_with_space with input from
        # multiline/tag_empty_input
        input_data = common.get_parser_input(
            'multiline/tag_empty_input',
        )

        result = parser.multiline.get_tags(input_data)

        # Then I see the results from
        # multiline/tag_empty_expected
        self.assertEqual(
            result,
            common.get_parser_output('multiline/tag_empty_expected'),
        )
