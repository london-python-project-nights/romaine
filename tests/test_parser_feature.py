from copy import deepcopy
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

    def test_getting_feature_no_input_modification(self):
        """
            Test that getting feature doesn't change the input var.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_feature with input from background/basic_input
        input_data = common.get_parser_input('feature/basic_input')

        expected_data = deepcopy(input_data)

        parser.feature.get_feature(input_data)

        # Then my input variable is not modified
        self.assertEqual(
            input_data,
            expected_data,
        )

    def test_get_feature(self):
        """
            Check we can get a feature.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_feature with input from background/basic_input
        input_data = common.get_parser_input('feature/basic_input')

        result = parser.feature.get_feature(input_data)

        # Then I see the results from feature/basic_expected
        self.assertEqual(
            result,
            common.get_parser_output('feature/basic_expected'),
        )

    def test_get_no_feature_trailing_noise(self):
        """
            Confirm exception raised when we don't end in something parseable.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_feature with input from background/just_noise_input
        input_data = common.get_parser_input('feature/just_noise_input')

        # Then I see a FeatureTrailingDataError
        with self.assertRaises(FeatureTrailingDataError):
            parser.feature.get_feature(input_data)
