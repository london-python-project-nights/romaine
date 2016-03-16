"""
Take a feature object, retrieve steps and run them all
"""
import importlib
import unittest

from tests.common import unload_test_data


class TestFeatureRunner(unittest.TestCase):

    def tearDown(self):
        unload_test_data()

    def test_full(self):
        # Given I have Romaine's core
        from romaine.core import Core
        core = Core()
        # And I have some step definitions
        importlib.import_module("test_data.steps.some_steps")
        # And I have a feature object
        feature = {}
        # When I run the feature
        statistics = core.run_feature(feature)
        # Then the output shows that the expected steps have been run
        assert statistics == {}
