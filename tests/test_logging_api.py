"""
We want a logger on the core, and the core should have methods to print out:

    [x] Error for an unimplemented step

    [x] Info for a finished step
    [x]     Info: step success
    [x]     Warning: step skipped
    [x]     Error: step failure

    [x] Info for a starting scenario
    [x] Info for a starting scenario outline
    [x] Info for a starting feature

    [x] Info for a scenario outline example:
    [x]     Info: example row success
    [x]     Warning: example row skipped
    [x]     Error: example row failure

    [ ] Run statistics
    [x]     Info: Total number of Features, Scenarios, Steps
    [x]     Info: Number of passed Features, Scenarios, Steps
    [x]     Info: Number of failed Steps
    [x]     Info: Number of skipped Steps
    [ ]     Debug: Duration of each Feature, Scenario, Step (debug)

    [x] Alert method actually does something
    [x]     Levels: logs to logging.Logger with appropriate log levels
    [x]     Text: can log text
    [x]     Exceptions: can log an exception given (exc_type, exc_val, exc_tb)

"""
import logging.handlers
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from romaine import logs
from romaine import exc


class TestRomaineLogger(logs.RomaineLogger):
    def __init__(self):
        super(TestRomaineLogger, self).__init__()
        handler = logging.handlers.BufferingHandler(float('inf'))
        self._stdlib_logger.addHandler(handler)
        self.records = handler.buffer


def given_a_test_step():
    """
    Given a test step
    """
    return {
        'leading_comments_and_space': [],
        'type': "Given",
        'text': "a test step",
        'multiline_arg': None,
        'trailing_whitespace': [],
    }


def given_a_test_scenario():
    """
    Scenario: Test Scenario
    """
    return {
        'leading_comments_and_space': [],
        'type': 'scenario',
        'tags': [],
        'description': ' Test Scenario',
        'steps': [given_a_test_step()],
    }


def given_a_feature():
    """
    Feature: Test Feature
    """
    return {
        'header': ['Feature: Test Feature'],
        'tags': [],
        'background': None,
        'leading_space_and_comments': [],
        'elements': [
            given_a_test_scenario_outline(),
            given_a_test_scenario_outline(),
        ],
        'trailing_space_and_comments': [],
    }


def given_a_test_scenario_outline():
    """
    Scenario Outline: Test Scenario Outline
        Given a number <num>
        Then I expect a word <word>
    Examples: Test Example
        | num | word |
        | 1   | one  |
    """
    return {
        'leading_comments_and_space': [],
        'type': 'scenario outline',
        'tags': [],
        'description': ' Test Scenario Outline',
        'steps': [
            {
                'leading_comments_and_space': ["    "],
                'type': "Given",
                'text': "a number <num>",
                'multiline_arg': None,
                'trailing_whitespace': [],
            },
            {
                'leading_comments_and_space': ["    "],
                'type': "Then",
                'text': "I expect word <word>",
                'multiline_arg': None,
                'trailing_whitespace': [],
            },
        ],
        'examples': [{
            'description': ' Test Example',
            'hashes': [
                {"num": "1", "word": "one"}
            ],
            'table': [
                [" num ", " word "],
                [" 1   ", " one  "]
            ],
            'leading_comments_and_space': [],
            'trailing_whitespace': [],
        }],
    }


def true_for_one_call(mock_fn, predicate):
    for (args, kwargs) in mock_fn.call_args_list:
        if predicate(*args, **kwargs):
            return True
    return False


class TestLoggingAPIUnimplementedStep(unittest.TestCase):

    @mock.patch('romaine.logs.RomaineLogger.alert')
    def test_error(self, mock_alert):
        # Given a test step
        step = given_a_test_step()
        # And a logger context
        with logs.RomaineLogger():
            # When I raise an error for the step not being implemented
            raise exc.UnimplementedStepError(step)

        # Then the logger alerts with an error
        def predicate(level, body='', exc_info=False):
            if level is logs.RomaineLogger.ERROR:
                try:
                    exc_type, exc_val, exc_tb = exc_info
                    # And the error alert contains the step dictionary
                    return getattr(exc_val, 'step') == step
                except:
                    return False
            return False

        assert true_for_one_call(mock_alert, predicate),\
            "No error found in alert calls!"

    @mock.patch('romaine.logs.RomaineLogger.alert')
    def test_stub(self, mock_alert):

        expected = (
            "@Given('a test step')\n"
            "def given_a_test_step():\n"
            "    raise NotImplementedError"
        )
        # Given a test step
        step = given_a_test_step()
        # And a logger context
        with logs.RomaineLogger():
            # When I raise an error for the step not being implemented
            raise exc.UnimplementedStepError(step)

        # Then the logger alerts with a stub for the step
        assert true_for_one_call(
            mock_alert,

            lambda level, body='', exc_info=False: (
                (level is logs.RomaineLogger.INFO) and
                (body == expected)
            )

        ), "No stub found in alert calls!"


class TestLoggingAPIFinishedStep(unittest.TestCase):

    @mock.patch('romaine.logs.RomaineLogger.alert')
    def test_success(self, mock_alert):

        # Given a logger context
        with logs.RomaineLogger() as logger:
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
                (level is logs.RomaineLogger.INFO) and
                (body == "Given a test step")
            )

        ), "No step as text found in alert calls!"

    @mock.patch('romaine.logs.RomaineLogger.alert')
    def test_skipping(self, mock_alert):

        # Given a logger context
        with logs.RomaineLogger() as logger:
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
                (level is logs.RomaineLogger.WARNING) and
                (body == "Given a test step (skipped)")
            )

        ), "No step as text found in alert calls!"

    @mock.patch('romaine.logs.RomaineLogger.alert')
    def test_failure(self, mock_alert):
        assertion_message = "Step failed!"

        # Given a logger context
        with logs.RomaineLogger() as logger:
            # And a test step
            step = given_a_test_step()
            # When I enter the step context
            with logger.in_step(step):
                # And I fail an assertion
                assert False, assertion_message

                # And I exit the step context

        # Then the logger alerts with an error with the step as text
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logs.RomaineLogger.ERROR) and
                (body == "Given a test step")
            )

        ), "No step as text found in alert calls!"

        def is_correct_exception(body):
            try:
                exc_type, exc_val, exc_tb = body
            except:
                return False

            return (
                isinstance(exc_val, AssertionError) and
                exc_val.args[0] == assertion_message
            )

        # And the logger alerts with an error with the exception information
        assert true_for_one_call(
            mock_alert,

            lambda level, body='', exc_info=False: (
                (level is logs.RomaineLogger.ERROR) and
                is_correct_exception(exc_info)
            )

        ), "No exception information found in alert calls!"


class TestLoggingAPIStartScenario(unittest.TestCase):

    @mock.patch('romaine.logs.RomaineLogger.alert')
    def test_start(self, mock_alert):

        # Given a logger context
        with logs.RomaineLogger() as logger:

            # And a test scenario
            scenario = given_a_test_scenario()
            # When I enter the scenario context
            with logger.in_scenario(scenario):
                # Then the logger alerts with information with the
                # scenario as text
                passed = true_for_one_call(
                    mock_alert,

                    lambda level, body: (
                        (level is logs.RomaineLogger.INFO) and
                        (body == "Scenario: Test Scenario")
                    )

                )

        assert passed, "No scenario as text found in alert calls!"


class TestLoggingAPIStartScenarioOutline(unittest.TestCase):

    @mock.patch('romaine.logs.RomaineLogger.alert')
    def test_start(self, mock_alert):

        # Given a logger context
        with logs.RomaineLogger() as logger:

            # And a test scenario outline
            scenario = given_a_test_scenario_outline()
            # When I enter the scenario outline context
            with logger.in_scenario_outline(scenario):
                # Then the logger alerts with information with the scenario
                # outline as text
                assert true_for_one_call(
                    mock_alert,

                    lambda level, body: (
                        (level is logs.RomaineLogger.INFO) and
                        (body == "Scenario Outline: Test Scenario Outline")
                    )
                ), "No scenario outline as text found in alert calls!"

                # And the logger alerts with information with the scenario
                # outline's steps as text
                assert true_for_one_call(
                    mock_alert,

                    lambda level, body: (
                        (level is logs.RomaineLogger.INFO) and
                        (body == "    Given a number <num>")
                    )
                ), "No 'Given' step found in alert calls!"
                assert true_for_one_call(
                    mock_alert,

                    lambda level, body: (
                        (level is logs.RomaineLogger.INFO) and
                        (body == "    Then I expect a word <word>")
                    )
                ), "No 'Then' step found in alert calls!"


class TestLoggingAPIStartFeature(unittest.TestCase):

    @mock.patch('romaine.logs.RomaineLogger.alert')
    def test_start(self, mock_alert):

        # Given a logger context
        with logs.RomaineLogger() as logger:

            # And a test feature
            feature = given_a_feature()
            # When I enter the feature context
            with logger.in_feature(feature):
                # Then the logger alerts with information with the feature as
                # text
                passed = true_for_one_call(
                    mock_alert,

                    lambda level, body: (
                        (level is logs.RomaineLogger.INFO) and
                        (body == "Feature: Test Feature")
                    )

                )

        assert passed, "No feature as text found in alert calls!"


class TestLoggingAPIScenarioOutlineExample(unittest.TestCase):

    @mock.patch('romaine.logs.RomaineLogger.alert')
    def test_success(self, mock_alert):

        # Given a test scenario outline
        outline = given_a_test_scenario_outline()
        # And a logger context
        with logs.RomaineLogger() as logger:
            # When I enter the scenario outline context
            with logger.in_scenario_outline(outline):
                # And I enter the first outline example context
                example = outline['examples'][0]
                with logger.in_scenario_outline_example(example):
                    # And I enter the first row's context
                    with logger.in_scenario_outline_example_row(
                        example, 0
                    ) as steps:
                        # And I enter the first step's context
                        step = steps[0]
                        # When I enter the step context
                        with logger.in_step(step, verbose=False):
                            # And I exit the first row's context
                            pass
                    # And I exit the first outline example context
                    pass
        # Then the logger alerts with information with the
        # example table heading
        if not true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logs.RomaineLogger.INFO) and
                ("Test Example" in body)
            )
        ): raise RuntimeError
        if not true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logs.RomaineLogger.INFO) and
                ("    | num | word |" in body)
            )
        ): raise RuntimeError
        # And the logger alerts with information with the scenario
        # outline example row as text
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logs.RomaineLogger.INFO) and
                (body == "    | 1   | one  |")
            )

        )

    @mock.patch('romaine.logs.RomaineLogger.alert')
    def test_skip(self, mock_alert):

        # Given a test scenario outline
        outline = given_a_test_scenario_outline()
        # And a logger context
        with logs.RomaineLogger() as logger:
            # When I enter the scenario outline context
            with logger.in_scenario_outline(outline):
                # And I enter the first outline example context
                example = outline['examples'][0]
                with logger.in_scenario_outline_example(example):
                    # And I enter the first row's context
                    with logger.in_scenario_outline_example_row(
                        example, 0
                    ) as steps:
                        # And I enter the first step's context
                        step = steps[0]
                        # When I enter the step context
                        with logger.in_step(step, verbose=False):
                            # And I raise a skip exception
                            raise exc.SkipTest
        # Then the logger alerts with information with the
        # example table heading
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logs.RomaineLogger.INFO) and
                ("Test Example" in body)
            )
        )
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logs.RomaineLogger.INFO) and
                ("    | num | word |" in body)
            )
        )
        # And the logger alerts with a warning with the scenario
        # outline example row as text
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logs.RomaineLogger.WARNING) and
                (body == "    | 1   | one  | (skipped)")
            )

        )

        # And the logger alerts with a warning with the step as text
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logs.RomaineLogger.WARNING) and
                (body == "Given a number 1 (skipped)")
            )

        ), "No step as text found in alert calls!"

    @mock.patch('romaine.logs.RomaineLogger.alert')
    def test_error(self, mock_alert):

        # Given a test scenario outline
        outline = given_a_test_scenario_outline()
        # And a logger context
        with logs.RomaineLogger() as logger:
            # When I enter the scenario outline context
            with logger.in_scenario_outline(outline):
                # And I enter the first outline example context
                example = outline['examples'][0]
                with logger.in_scenario_outline_example(example):
                    # And I enter the first row's context
                    with logger.in_scenario_outline_example_row(
                        example, 0
                    ) as steps:
                        # And I enter the first step's context
                        step = steps[0]
                        # When I enter the step context
                        with logger.in_step(step, verbose=False):
                            # And I raise a skip exception
                            assert False
        # Then the logger alerts with information with the
        # example table heading
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logs.RomaineLogger.INFO) and
                ("Test Example" in body)
            )
        )
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logs.RomaineLogger.INFO) and
                ("    | num | word |" in body)
            )
        )
        # And the logger alerts with a warning with the scenario
        # outline example row as text
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logs.RomaineLogger.ERROR) and
                (body == "    | 1   | one  |")
            )

        )

        # And the logger alerts with a warning with the step as text
        assert true_for_one_call(
            mock_alert,

            lambda level, body: (
                (level is logs.RomaineLogger.ERROR) and
                (body == "Given a number 1")
            )

        ), "No step as text found in alert calls!"


class TestLoggingAPIAlertMethod(unittest.TestCase):

    def _test_log_level_text(self, level_in, message, level_out):
        # Given a logger context
        with TestRomaineLogger() as logger:
            # When I output an <level_in> message
            logger.alert(level_in, message)
        # Then I see a <level_out> message from the std library logger

        for record in logger.records:
            if record.levelno == level_out and record.msg == message:
                return

        assert not logger.records, "No matching record found"

    def test_info(self):
        self._test_log_level_text(
            level_in=TestRomaineLogger.INFO,
            message="Hello, World!",
            level_out=logging.INFO,
        )

    def test_warn(self):
        self._test_log_level_text(
            level_in=TestRomaineLogger.WARNING,
            message="Hello, World!",
            level_out=logging.WARNING,
        )

    def test_error(self):
        self._test_log_level_text(
            level_in=TestRomaineLogger.ERROR,
            message="Hello, World!",
            level_out=logging.ERROR,
        )

    def test_record_assertions(self):
        message = "Woops!"

        # Given a logger context
        with TestRomaineLogger() as logger:
            # When I raise an assertion
            assert False, message
        # Then I see a ERROR message from the std library logger with the
        # traceback attached

        for record in logger.records:
            if all((
                record.levelno == logging.ERROR,
                record.exc_info,
                isinstance(record.exc_info[1], AssertionError),
                record.exc_info[1].args[0] == message
            )):
                return

        assert not logger.records, "No matching record found"

    def test_record_runtime_error(self):
        message = "Woops!"
        exc_type = RuntimeError

        try:
            # Given a logger context
            with TestRomaineLogger() as logger:
                # When I raise an assertion
                raise exc_type(message)
        except exc_type:
            pass

        # Then I see a ERROR message from the std library logger with the
        # traceback attached
        for record in logger.records:
            if all((
                    record.levelno == logging.ERROR,
                    record.exc_info,
                    isinstance(record.exc_info[1], exc_type),
                    record.exc_info[1].args[0] == message
            )):
                return

        assert False, "No matching record found"


class TestLoggingAPIStatistics(unittest.TestCase):

    def _fail(self):
        assert False

    def _skip(self):
        raise exc.SkipTest

    def _run_for_steps(self, fn=None):
        """
        yields the logger context, then runs fn for each step
        """
        # Given a logger context
        with TestRomaineLogger() as logger:
            yield logger
            # And a test feature
            feature = given_a_feature()
            # When I enter the feature context
            with logger.in_feature(feature):
                # Given each scenario outline in the feature
                for scenario in feature["elements"]:
                    # When I enter the scenario outline context
                    with logger.in_scenario_outline(scenario):
                        # Given each example in the scenario outline
                        for example in scenario["examples"]:
                            # When I enter the example context
                            with logger.in_scenario_outline_example(example):
                                # Given each row in the example
                                for index in range(len(example["hashes"])):
                                    with logger\
                                        .in_scenario_outline_example_row(
                                            example, index) as run:
                                        for step in run:
                                            with logger.in_step(step):
                                                if fn is not None:
                                                    fn()

    def test_total_stats(self):
        for logger in self._run_for_steps():
            pass

        assert logger.statistics["features"]["total"] == 1
        assert logger.statistics["scenarios"]["total"] == 2
        assert logger.statistics["steps"]["total"] == 4

        looking_for = {
            "1 feature",
            "2 scenarios",
            "4 steps",
        }

        for record in logger.records:
            if record.levelno == logging.INFO:
                looking_for_ = list(looking_for)
                for message in looking_for_:
                    if message in record.msg:
                        looking_for.remove(message)
                if not looking_for:
                    return
        assert False, "Stats not found: {}".format(looking_for)

    def test_passed_stats(self):
        for logger in self._run_for_steps():
            pass

        assert logger.statistics["features"]["passed"] == 1
        assert logger.statistics["scenarios"]["passed"] == 2
        assert logger.statistics["steps"]["passed"] == 4

        looking_for = {
            "1 feature (1 passed)",
            "2 scenarios (2 passed)",
            "4 steps (4 passed)",
        }

        for record in logger.records:
            if record.levelno == logging.INFO:
                looking_for_ = list(looking_for)
                for message in looking_for_:
                    if message in record.msg:
                        looking_for.remove(message)
                if not looking_for:
                    return
        assert False, "Stats not found: {}".format(looking_for)

    def test_failed_stats(self):
        for logger in self._run_for_steps(self._fail):
            pass

        assert logger.statistics["features"]["passed"] == 0
        assert logger.statistics["scenarios"]["passed"] == 0
        assert logger.statistics["steps"]["passed"] == 0
        assert logger.statistics["steps"]["failed"] == 2

        looking_for = {
            "1 feature (0 passed)",
            "2 scenarios (0 passed)",
            "4 steps (2 failed, 0 passed)",
        }

        for record in logger.records:
            if record.levelno == logging.INFO:
                looking_for_ = list(looking_for)
                for message in looking_for_:
                    if message in record.msg:
                        looking_for.remove(message)
                if not looking_for:
                    return
        assert False, "Stats not found: {}".format(looking_for)

    def test_skipped_stats(self):
        for logger in self._run_for_steps(self._skip):
            pass

        assert logger.statistics["features"]["passed"] == 0
        assert logger.statistics["scenarios"]["passed"] == 0
        assert logger.statistics["steps"]["passed"] == 0
        assert logger.statistics["steps"]["skipped"] == 2

        looking_for = {
            "1 feature (0 passed)",
            "2 scenarios (0 passed)",
            "4 steps (2 skipped, 0 passed)",
        }

        for record in logger.records:
            if record.levelno == logging.INFO:
                looking_for_ = list(looking_for)
                for message in looking_for_:
                    if message in record.msg:
                        looking_for.remove(message)
                if not looking_for:
                    return
        assert False, "Stats not found: {}".format(looking_for)
