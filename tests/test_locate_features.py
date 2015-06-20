from tests import common  # noqa
from tests import exceptions
import os
import unittest


class TestLocateFeatures(unittest.TestCase):
    """
        Test feature location functionality of romaine's core.
    """
    feature_paths = ('tests/features',
                     '/tmp/romaine_tests/features')
    features = ('feature1',
                'feature2',
                'subdir/feature3')

    def setUp(self):
        """
            Prepare the environment for testing.
        """
        # Running as root may result in an attempt later to remove /tmp
        if os.geteuid() == 0:
            raise exceptions.RunningAsRootError(
                'Running as root may be harmful, aborting.'
                )

        for base_path in self.feature_paths:
            try:
                os.makedirs(os.path.join(base_path, 'subdir'))
            except OSError:
                # Path exists, good.
                pass

            for feature in self.features:
                with open(os.path.join(base_path, feature), 'a'):
                    # We don't need to write anything, just create the file
                    pass

    def tearDown(self):
        """
            Revert changes made during testing.
        """
        for base_path in self.feature_paths:
            # Remove the feature files
            for feature in self.features:
                feature = os.path.join(base_path, feature)
                os.remove(feature)

            # Attempt to remove all the directories we created
            os.removedirs(os.path.join(base_path, 'subdir'))

    def test_features_found_by_relative_path(self):
        """
            Check we can find features by a relative path.
        """
        # Given I have Romaine's core
        from tests.common import romaine
        core = romaine.Core()

        # When I locate features in tests/features
        results = core.locate_features('tests/features')

        # Then I see the list:
        #   | path                           |
        #   | tests/features/feature1        |
        #   | tests/features/feature2        |
        #   | tests/features/subdir/feature3 |
        self.assertEqual(
            sorted(results),
            [
                'tests/features/feature1',
                'tests/features/feature2',
                'tests/features/subdir/feature3',
                ]
            )

    def test_features_found_by_absolute_path(self):
        """
            Check we can find features by an absolute path.
        """
        # Given I have Romaine's core
        from tests.common import romaine
        core = romaine.Core()

        # When I locate features in /tmp/romaine_tests/features
        results = core.locate_features('/tmp/romaine_tests/features')

        # Then I see the list:
        #   | path                           |
        #   | /tmp/romaine_tests/features/feature1        |
        #   | /tmp/romaine_tests/features/feature2        |
        #   | /tmp/romaine_tests/features/subdir/feature3 |
        self.assertEqual(
            sorted(results),
            [
                '/tmp/romaine_tests/features/feature1',
                '/tmp/romaine_tests/features/feature2',
                '/tmp/romaine_tests/features/subdir/feature3',
                ],
            )

    def test_multiple_calls_no_duplicates(self):
        """
            Confirm no duplicates for two calls with the same path.
        """
        # Given I have Romaine's core
        from tests.common import romaine
        core = romaine.Core()

        # When I locate features in /tmp/romaine_tests/features
        core.locate_features('/tmp/romaine_tests/features')
        #  And I locate features in /tmp/romaine_tests/features
        core.locate_features('/tmp/romaine_tests/features')

        # Then the core's feature_paths_list variable contains no duplicates
        feature_file_paths = list(core.feature_file_paths)
        for item in feature_file_paths:
            self.assertEqual(
                feature_file_paths.count(item),
                1,
                )

    def test_confirm_features_in_class_variable(self):
        """
            Check feature location populates class features variable.
        """
        # Given I have Romaine's core
        from tests.common import romaine
        core = romaine.Core()

        # When I locate features in /tmp/romaine_tests/features
        #  And I locate features in tests/features
        core.locate_features('/tmp/romaine_tests/features')
        core.locate_features('tests/features')

        # Then the core's feature_paths_list variable contains:
        #   | path                                        |
        #   | /tmp/romaine_tests/features/feature1        |
        #   | /tmp/romaine_tests/features/feature2        |
        #   | /tmp/romaine_tests/features/subdir/feature3 |
        #   | tests/features/feature1                     |
        #   | tests/features/feature2                     |
        #   | tests/features/subdir/feature3              |
        self.assertEqual(
            sorted(core.feature_file_paths),
            [
                '/tmp/romaine_tests/features/feature1',
                '/tmp/romaine_tests/features/feature2',
                '/tmp/romaine_tests/features/subdir/feature3',
                'tests/features/feature1',
                'tests/features/feature2',
                'tests/features/subdir/feature3',
                ]
            )
