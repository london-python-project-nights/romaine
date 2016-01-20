"""
We want a logger on the core, and the core should have methods to print out:

    [x] Error for an unimplemented step

    [x] Info for a finished step
    [x]     Info: step success
    [x]     Warning: step skipped
    [x]     Error: step failure

    [ ] Info for a finished scenario
    [ ]     Info: scenario success
    [ ]     Warning: scenario skipped
    [ ]     Error: scenario failure

    [ ] Info for a finished scenario outline
    [ ]     Info: scenario outline success
    [ ]     Warning: scenario outline skipped
    [ ]     Error: scenario outline failure

    [ ] Info for a finished feature
    [ ]     Info: feature success
    [ ]     Warning: feature skipped
    [ ]     Error: feature failure

    [ ] Run statistics
    [ ]     Info: Total number of Features, Scenarios, Steps
    [ ]     Info: Number of passed Features, Scenarios, Steps
    [ ]     Info: Number of failed Features, Scenarios, Steps
    [ ]     Info: Number of skipped Features, Scenarios, Steps
    [ ]     Debug: Duration of each Feature, Scenario, Step (debug)

    [ ] Some debug level output for the feature/step finding:
    [ ]     Debug: Searching for features in , found , are acceptable as features.
    [ ]     Debug: Obtained steps from .
    [ ]     Debug: Asked to run step with string by feature , selected step
    [ ]     Warn: Empty feature files

    [ ] Alert method actually does something
    [ ]     Levels: logs to logging.Logger with appropriate log levels
    [ ]     Text: can log text
    [ ]     Exceptions: can log an exception given (exc_type, exc_val, exc_tb)

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
                try:
                    exc_type, exc_val, exc_tb = body
                    # And the error alert contains the step dictionary
                    return getattr(exc_val, 'step') == step
                except:
                    return False
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

    @mock.patch('romaine.logging.RomaineLogger.alert')
    def test_failure(self, mock_alert):

        # Given a logger context
        with logging.RomaineLogger() as logger:
            # And a test step
            step = given_a_test_step()
            # When I enter the step context
            with logger.in_step(step):
                # And I raise an exception
                expected_exception_object = RuntimeError("Boo!")

                raise expected_exception_object

                # And I exit the step context

        # Then the logger alerts with an error with the step as text
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logging.RomaineLogger.ERROR) and
                (body == "Given a test step")
            )

        ), "No step as text found in alert calls!"

        def is_correct_exception(body):
            try:
                exc_type, exc_val, exc_tb = body
            except:
                return False

            return exc_val is expected_exception_object

        # And the logger alerts with an error with the exception information
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logging.RomaineLogger.ERROR) and
                is_correct_exception(body)
            )

        ), "No exception information found in alert calls!"
