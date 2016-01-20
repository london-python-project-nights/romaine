"""
We want a logger on the core, and the core should have methods to print out:

    [x] Error for an unimplemented step

    [ ] Info for a finished step
    [x]     Info for step success
    [x]     Warning for step skipped
    [ ]     Error for step failure

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


class TestLoggingAPIUnimplementedStep(unittest.TestCase):

    @mock.patch('romaine.logging.RomaineLogger.alert')
    def test_nothing_logged(self, mock_alert):

        # Given a logger context
        with logging.RomaineLogger():
            # When I don't use the logger
            pass
        # Then the logger does not alert
        assert not mock_alert.called

    @mock.patch('romaine.logging.RomaineLogger.alert')
    def test_error(self, mock_alert):
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
            return False

        assert true_for_one_call(mock_alert, predicate),\
            "No error found in alert calls!"

    @mock.patch('romaine.logging.RomaineLogger.alert')
    def test_stub(self, mock_alert):

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

        # Then the logger alerts with a stub for the step
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logging.RomaineLogger.INFO) and
                (body == expected)
            )

        ), "No stub found in alert calls!"


class TestLoggingAPIFinishedStep(unittest.TestCase):

    @mock.patch('romaine.logging.RomaineLogger.alert')
    def test_success(self, mock_alert):

        # Given a logger context
        with logging.RomaineLogger() as logger:
            # And a test step
            step = given_a_test_step()
            # When I enter the step context
            with logger.in_step(step):
                # And I exit the step context
                pass

        # Then the logger alerts with information with the step as text
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logging.RomaineLogger.INFO) and
                (body == "Given a test step")
            )

        ), "No step as text found in alert calls!"

    @mock.patch('romaine.logging.RomaineLogger.alert')
    def test_skipping(self, mock_alert):

        # Given a logger context
        with logging.RomaineLogger() as logger:
            # And a test step
            step = given_a_test_step()
            # When I enter the step context
            with logger.in_step(step):
                # And I raise a skip exception
                raise exc.SkipTest

                # And I exit the step context

        # Then the logger alerts with a warning with the step as text
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logging.RomaineLogger.WARNING) and
                (body == "Given a test step (skipped)")
            )

        ), "No step as text found in alert calls!"


    # @mock.patch('romaine.logging.RomaineLogger.alert')
    # def test_failure(self, mock_alert):
    #
    #     # Given a logger context
    #     with logging.RomaineLogger():
    #         # And a test step
    #         step = given_a_test_step()
    #         # When I enter the step context
    #         # And I raise an exception
    #         # And I exit the step context
    #         # Then the logger alerts with an error
    #         # And I expect to see the step as text
    #         # And I expect to see the exception information
    #
    #     raise NotImplementedError
