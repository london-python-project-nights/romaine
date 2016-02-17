from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
import logging

from romaine import exc


def test_step_to_stub(step):

    step_chars = set(step["text"])

    step_slug = "{type}_{text}".format(**step).lower()
    for char in step_chars:
        if not char.isalnum():
            step_slug = step_slug.replace(char, "_")

    return "\n".join([
        "@{type}({text!r})".format(**step),
        "def {step_slug}():".format(step_slug=step_slug),
        "    raise NotImplementedError"
    ])


# TODO - This should be in the runner, but that is not built yet
def fill_step_with_example_row(step, row):
    step_text = step['text']

    for key, value in row.items():
        step_text = step_text.replace("<{key}>".format(key=key), value)

    step = step.copy()
    step['text'] = step_text

    return step


class AbstractRomaineLogger(object):
    __metaclass__ = ABCMeta

    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR

    def __init__(self):
        self._feature = None
        self._scenario = None
        self._scenario_outline = None
        self._scenario_outline_example = None
        self._step = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        We want to make sure that any exceptions thrown are logged,
        unless it's a SkipTest which will have already been warned
        about.

        We also want to mark SkipTest, UnimplementedStepError, and
        AssertionError as having been handled so they don't abort the
        test run. Any other exception will be logged, but not handled.
        """
        if exc_val is not None:
            if isinstance(exc_val, exc.SkipTest):
                return True
            else:
                self.alert(self.ERROR, exc_info=(exc_type, exc_val, exc_tb))

            if isinstance(exc_val, exc.UnimplementedStepError):
                stub = test_step_to_stub(exc_val.step)
                self.alert(self.INFO, stub)
                return True
            elif isinstance(exc_val, AssertionError):
                return True

    @contextmanager
    def in_step(self, step, verbose=True):
        self._step = step
        try:
            yield
        except exc.SkipTest:
            self.alert(self.WARNING, "{type} {text} (skipped)".format(**step))
            raise
        except AssertionError:
            self.alert(self.ERROR, "{type} {text}".format(**step))
            raise
        else:
            self.alert(self.INFO if verbose else self.WARNING,
                       "{type} {text}".format(**step))
        finally:
            self._step = None

    @contextmanager
    def in_scenario(self, scenario):
        self._scenario = scenario
        self.alert(self.INFO, "Scenario:{description}".format(**scenario))
        try:
            yield
        except exc.SkipTest:
            pass
        finally:
            self._scenario = None

    @contextmanager
    def in_scenario_outline(self, scenario_outline):
        self._scenario_outline = scenario_outline
        self.alert(self.INFO,
                   "Scenario Outline:{description}".format(**scenario_outline))
        try:
            yield
        except exc.SkipTest:
            pass
        finally:
            self._scenario_outline = None

    @contextmanager
    def in_scenario_outline_example(self, scenario_outline_example):
        self._scenario_outline_example = scenario_outline_example
        self._scenario_outline_example_row_index = 0

        headings = scenario_outline_example['table'][0]
        heading_row = "|".join(headings)

        self.alert(
            self.INFO,
            "Example:{description}\n"
            "    |{heading_row}|"
            .format(heading_row=heading_row, **scenario_outline_example)
        )

        try:
            yield
        finally:
            del self._scenario_outline_example_row_index
            self._scenario_outline = None

    @contextmanager
    def in_scenario_outline_example_row(self, row):
        self.alert(self.INFO, "    |{}|".format("|".join(row)))
        try:
            yield
        except exc.SkipTest:
            self.alert(self.WARNING,
                       "    |{}| (skipped)".format("|".join(row)))
        except AssertionError:
            self.alert(self.ERROR,
                       "    |{}|".format("|".join(row)))
            raise

    @contextmanager
    def in_feature(self, feature):
        self._feature = feature
        self.alert(self.INFO, "\n".join(feature["header"]))
        try:
            yield
        finally:
            self._feature = None

    @abstractmethod
    def alert(self, level, body='', exc_info=False):
        pass


class RomaineLogger(AbstractRomaineLogger):

    def __init__(self):
        super(RomaineLogger, self).__init__()
        self._stdlib_logger = logging.Logger(str(self))

        self._levels = {
            self.INFO: self._stdlib_logger.info,
            self.WARNING: self._stdlib_logger.warning,
            self.ERROR: self._stdlib_logger.error,
        }

    def alert(self, level, body='', exc_info=False):

        if level not in self._levels:
            raise NotImplementedError

        self._levels[level](body, exc_info=exc_info)