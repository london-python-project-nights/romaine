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
        self._scenario_outline = None
        self._scenario_outline_example = None
        self.statistics = None

    def __enter__(self):
        self.statistics = {
            "features": {
                "total": 0,
                "passed": 0,
            },
            "scenarios": {
                "total": 0,
                "passed": 0,
            },
            "steps": {
                "total": 0,
                "passed": 0,
                "skipped": 0,
                "failed": 0,
            },
        }
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
        handle = False

        if exc_val is not None:
            if isinstance(exc_val, exc.SkipTest):
                handle = True
            else:
                self.alert(self.ERROR, exc_info=(exc_type, exc_val, exc_tb))

            if isinstance(exc_val, exc.UnimplementedStepError):
                stub = test_step_to_stub(exc_val.step)
                self.alert(self.INFO, stub)
                handle = True
            elif isinstance(exc_val, AssertionError):
                handle = True

        self._log_stats()

        if handle:
            return True

    def _log_stats(self):
        if "features" in self.statistics:
            feature = self.statistics["features"]
            total = feature.get("total", 0)
            passed = feature.get("passed", 0)
            word = "feature" if total is 1 else "features"

            self.alert(
                self.INFO,
                "{} {} ({} passed)".format(
                    total,
                    word,
                    passed,
                )
            )
        if "scenarios" in self.statistics:
            scenarios = self.statistics["scenarios"]
            total = scenarios.get("total", 0)
            passed = scenarios.get("passed", 0)
            word = "scenario" if total is 1 else "scenarios"
            self.alert(
                self.INFO,
                "{} {} ({} passed)".format(
                    total,
                    word,
                    passed,
                )
            )
        if "steps" in self.statistics:
            steps = self.statistics["steps"]
            word = "step" if total is 1 else "steps"
            parts = []

            failed = steps.get("failed", 0)

            if failed:
                parts.append("{} failed".format(failed))

            skipped = steps.get("skipped", 0)

            if skipped:
                parts.append("{} skipped".format(skipped))

            parts.append("{} passed".format(steps.get("passed", 0)))

            self.alert(
                self.INFO,
                "{} {} ({})".format(
                    steps.get("total", 0),
                    word,
                    ', '.join(parts),
                )
            )

    @contextmanager
    def in_step(self, step, verbose=True):
        step["stats"] = {
            "passed": False,
            "failed": False,
            "skipped": False,
        }

        try:
            yield
        except exc.SkipTest:
            self.alert(self.WARNING, "{type} {text} (skipped)".format(**step))
            step["stats"]["skipped"] = True
            raise
        except AssertionError:
            self.alert(self.ERROR, "{type} {text}".format(**step))
            step["stats"]["failed"] = True
            raise
        except:
            step["stats"]["failed"] = True
            raise
        else:
            self.alert(self.INFO if verbose else self.WARNING,
                       "{type} {text}".format(**step))
            step["stats"]["passed"] = True

    @staticmethod
    def _collect_scenario_stats(scenario, steps):
        scenario["stats"] = stats = {
            "passed_steps": 0,
            "failed_steps": 0,
            "skipped_steps": 0,
            "total_steps": 0,
            "passed": False,
            "failed": False,
        }
        for step in steps:
            stats["total_steps"] += 1
            step_stats = step.get("stats")
            if step_stats is None:
                pass
            elif step_stats["passed"]:
                stats["passed_steps"] += 1
            elif step_stats["failed"]:
                stats["failed_steps"] += 1
            elif step_stats["skipped"]:
                stats["skipped_steps"] += 1

        if stats["failed_steps"]:
            stats["failed"] = True
        elif stats["passed_steps"]:
            stats["passed"] = True

    @contextmanager
    def in_scenario(self, scenario):
        self.alert(self.INFO, "Scenario:{description}".format(**scenario))
        try:
            yield
        except exc.SkipTest:
            pass
        finally:
            self._collect_scenario_stats(scenario, scenario["steps"])

    def _scenario_outline_steps(self):
        for example in self._scenario_outline["examples"]:
            for run in example.get("runs", ()):
                for step in run:
                    yield step

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
            self._collect_scenario_stats(scenario_outline,
                                         self._scenario_outline_steps())
            self._scenario_outline = None

    @contextmanager
    def in_scenario_outline_example(self, scenario_outline_example):
        self._scenario_outline_example = scenario_outline_example
        self._scenario_outline_example["runs"] = []

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
            self._scenario_outline_example = None

    @contextmanager
    def in_scenario_outline_example_row(self, example, index):
        row_string = example["table"][index + 1]
        row_dict = example["hashes"][index]
        run = [
            fill_step_with_example_row(step, row_dict)
            for step in self._scenario_outline["steps"]
        ]
        self._scenario_outline_example["runs"].append(run)
        self.alert(self.INFO, "    |{}|".format("|".join(row_string)))
        try:
            yield run
        except exc.SkipTest:
            self.alert(self.WARNING,
                       "    |{}| (skipped)".format("|".join(row_string)))
        except AssertionError:
            self.alert(self.ERROR,
                       "    |{}|".format("|".join(row_string)))

    @abstractmethod
    def alert(self, level, body='', exc_info=False):
        pass

    @contextmanager
    def in_feature(self, feature):
        self._feature = feature
        feature["stats"] = {
            "passed_steps": 0,
            "failed_steps": 0,
            "skipped_steps": 0,
            "total_steps": 0,
            "passed_scenarios": 0,
            "failed_scenarios": 0,
            "total_scenarios": 0,
            "passed": False,
            "failed": False,
        }
        self.alert(self.INFO, "\n".join(feature["header"]))
        try:
            yield
        finally:
            self._collect_feature_stats(feature)
            self._feature = None

    def _collect_feature_stats(self, feature):
        stats = feature["stats"]
        self.statistics["features"]["total"] += 1

        for scenario in feature["elements"]:
            stats["total_scenarios"] += 1

            scenario_stats = scenario.get("stats")
            if scenario_stats is None:
                # If for some reason the scenario hasn't run, don't
                # try to collect its stats
                continue

            for key in (
                "passed_steps",
                "failed_steps",
                "skipped_steps",
                "total_steps",
            ):
                stats[key] += scenario_stats.get(key, 0)

            self.statistics["scenarios"]["total"] += 1

            if scenario_stats.get("passed"):
                stats["passed_scenarios"] += 1
                self.statistics["scenarios"]["passed"] += 1
            elif scenario_stats.get("failed"):
                stats["failed_scenarios"] += 1

        self.statistics["steps"]["skipped"] += stats["skipped_steps"]
        self.statistics["steps"]["passed"] += stats["passed_steps"]
        self.statistics["steps"]["failed"] += stats["failed_steps"]
        self.statistics["steps"]["total"] += stats["total_steps"]

        if stats["failed_scenarios"]:
            stats["failed"] = True
        elif stats["passed_scenarios"]:
            stats["passed"] = True
            self.statistics["features"]["passed"] += 1


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
