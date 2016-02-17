import sys
from contextlib import contextmanager

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


class RomaineLogger(object):

    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

    def __init__(self):
        self._feature = None
        self._scenario = None
        self._scenario_outline = None
        self._scenario_outline_example = None
        self._step = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, exc.UnimplementedStepError):
            self.alert(self.ERROR, (exc_type, exc_val, exc_tb))
            stub = test_step_to_stub(exc_val.step)
            self.alert(self.INFO, stub)
        elif isinstance(exc_val, AssertionError):
            self.alert(self.ERROR, (exc_type, exc_val, exc_tb))
        else:
            return
        return True

    @contextmanager
    def in_step(self, step):
        self._step = step
        try:
            yield
        except exc.SkipTest:
            self.alert(self.WARNING, "{type} {text} (skipped)".format(**step))
        except AssertionError:
            self.alert(self.ERROR, "{type} {text}".format(**step))
            self.alert(self.ERROR, sys.exc_info())
        else:
            self.alert(self.INFO, "{type} {text}".format(**step))
        finally:
            self._step = None

    @contextmanager
    def in_scenario(self, scenario):
        self._scenario = scenario
        self.alert(self.INFO, "Scenario:{description}".format(**scenario))
        try:
            yield
        finally:
            self._scenario = None

    @contextmanager
    def in_scenario_outline(self, scenario_outline):
        self._scenario_outline = scenario_outline
        self.alert(self.INFO,
                   "Scenario Outline:{description}".format(**scenario_outline))
        try:
            yield
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
        yield

    @contextmanager
    def in_feature(self, feature):
        self._feature = feature
        self.alert(self.INFO, "\n".join(feature["header"]))
        try:
            yield
        finally:
            self._feature = None

    def alert(self, level, body):
        pass
