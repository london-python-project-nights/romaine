"""
We want a logger on the core, and the core should have methods to print out:

    [x] Error for an unimplemented step
    [ ] Error for step failure
    [ ] Info for a running step
    [ ] Info for step success
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


def given_a_test_step():
    return {
        'leading_comments_and_space': [],
        'type': "Given",
        'text': "a test step",
        'multiline_arg': None,
        'trailing_whitespace': [],
    }


def true_for_one_call(mock_fn, predicate):
    for (args, kwargs) in mock_fn.call_args_list:
        if predicate(*args, **kwargs):
            return True
    return False


class TestLoggingAPI(unittest.TestCase):

    @mock.patch('romaine.logging.RomaineLogger.alert')
    def test_nothing_logged(self, mock_alert):

        # Given a logger context
        with logging.RomaineLogger():
            # When I don't use the logger
            pass
        # Then the logger does not alert
        assert not mock_alert.called

    @mock.patch('romaine.logging.RomaineLogger.alert')
    def test_unimplemented_step_error(self, mock_alert):
        # Given a test step
        step = given_a_test_step()
        # And a logger context
        with logging.RomaineLogger():
            # When I raise an error for the step not being implemented
            raise exc.UnimplementedStepError(step)

        # Then the logger alerts with an error
        def predicate(level, body):
            if level is logging.RomaineLogger.ERROR:
                exc_type, exc_val, exc_tb = body
                # And the error alert contains the step dictionary
                return getattr(exc_val, 'step') == step

        assert true_for_one_call(mock_alert, predicate),\
            "No error found in alert calls!"

    @mock.patch('romaine.logging.RomaineLogger.alert')
    def test_unimplemented_step_stub(self, mock_alert):

        expected = (
            "@Given('a test step')\n"
            "def given_a_test_step():\n"
            "    raise NotImplementedError"
        )
        # Given a test step
        step = given_a_test_step()
        # And a logger context
        with logging.RomaineLogger():
            # When I raise an error for the step not being implemented
            raise exc.UnimplementedStepError(step)

        # Then the logger alerts with information
        def predicate(level, body):
            if level is logging.RomaineLogger.INFO:
                # And the info alert contains a stub for the step
                return body == expected

        assert true_for_one_call(mock_alert, predicate),\
            "No stub found in alert calls!"

