"""
We want a logger on the core, and the core should have methods to print out:

    [ ] Error for an unimplemented step
    [ ] Info for a running step
    [ ] Info for step success
    [ ] Error for step failure
    [ ] Warning for step skipped
    [ ] Run statistics
    [ ]     Total number of Features, Scenarios, Steps
    [ ]     Number of passed Features, Scenarios, Steps
    [ ]     Number of failed Features, Scenarios, Steps
    [ ]     Number of skipped Features, Scenarios, Steps
    [ ]     Duration of each Feature, Scenario, Step (debug)
    [ ] Some debug level output for the feature/step finding:
    [ ]     DEBUG: Searching for features in , found , are acceptable as features.
    [ ]     DEBUG: Obtained steps from .
    [ ]     DEBUG: Asked to run step with string by feature , selected step
    [ ]     Warn for empty feature files

"""
import unittest

from unittest import mock

from romaine import logging
from romaine import exc



class TestLoggingAPI(unittest.TestCase):

    # Todo - test that UnimplementedStepException contains step info

    @mock.patch('romaine.logging.RomaineLogger.alert')
    def test_unimplemented_step_error(self, mock_alert):

        # Given a logger context
        with logging.RomaineLogger():
            # When I raise an error for a missing feature step implementation
            raise exc.UnimplementedStepError
        # Then the logger alerts with an error
        assert mock_alert.called

        for (obj, level, body) in mock_alert.call_args_list:
            if level is logging.RomaineLogger.ERROR:
                break
        else:
            raise RuntimeError("No error found in alert calls!")

    def test_unimplemented_step_stub(self):

        # Todo - work out what we want to do with this info

        # Given a logger context
        # When I raise an error for a missing feature step implementation
        # Then the logger alerts with information

        raise NotImplementedError

