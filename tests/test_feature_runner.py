"""
Take a feature object, retrieve steps and run them all
"""
import importlib
import unittest

from tests.common import unload_test_data


class StepStatus:
    class _Status(object):
        def __init__(self, status_string):
            self.status_string = status_string

        def __call__(self, status_object):
            return status_object.status_string == self.status_string

    passed = _Status("passed")
    failed = _Status("failed")
    skipped = _Status("skipped")
    not_reached = _Status("not_reached")


def make_feature(name="Feature: Test Feature", **custom):
    feature = {
        'header': [name],
        'tags': [],
        'background': None,
        'leading_space_and_comments': [],
        'elements': [],
        'trailing_space_and_comments': [],
    }
    feature.update(custom)
    return feature


def make_scenario(**custom):
    scenario = {
        'leading_comments_and_space': [],
        'type': 'scenario',
        'tags': [],
        'description': ' Test Scenario',
        'steps': [],
    }
    scenario.update(custom)
    return scenario


def make_step(text="step_name", **custom):
    step = {
        'leading_comments_and_space': [],
        'type': "Given",
        'text': text,
        'multiline_arg': None,
        'trailing_whitespace': [],
    }
    step.update(custom)
    return step


def given_i_have_a_feature_object(steps):
    return make_feature(elements=[
        make_scenario(steps=[
            make_step(type=step_type, text=step_text)
            for (step_type, step_text, _) in steps
        ])
    ])


def check_stats(statistics, steps):
    step_stats = {"total": 0, "passed": 0, "skipped": 0, "failed": 0}
    for (_, __, status) in steps:
        step_stats["total"] += 1

        if StepStatus.passed(status):
            step_stats["passed"] += 1
        elif StepStatus.skipped(status):
            step_stats["skipped"] += 1
        elif StepStatus.failed(status):
            step_stats["failed"] += 1

    all_passed = step_stats["passed"] == step_stats["total"]
    assert statistics["scenarios"] == {
        "total": 1,
        "passed": 1 if all_passed else 0,
    }
    assert statistics["steps"] == step_stats
    for key, expected in {
        "total": 1,
        "passed": 1 if all_passed else 0,
    }.items():
        assert statistics["features"][key] == expected
    assert len(statistics["features"]["run"]) == 1
    feature = statistics["features"]["run"][0]
    feature_stats = feature["stats"]
    for key, expected in {
        "passed_steps": step_stats["passed"],
        "failed_steps": step_stats["failed"],
        "skipped_steps": step_stats["skipped"],
        "total_steps": step_stats["total"],
        "passed_scenarios": 1 if all_passed else 0,
        "failed_scenarios": 0 if all_passed else 1,
        "total_scenarios": 1,
        "passed": all_passed is True,
        "failed": all_passed is not True,
    }.items():
        assert feature_stats[key] == expected
    assert len(feature["elements"]) == 1
    scenario = feature["elements"][0]
    scenario_stats = scenario["stats"]
    for key, expected in {
        "passed_steps": step_stats["passed"],
        "failed_steps": step_stats["failed"],
        "skipped_steps": step_stats["skipped"],
        "total_steps": step_stats["total"],
        "passed": all_passed is True,
        "failed": all_passed is not True,
    }.items():
        assert scenario_stats[key] == expected
    for step_details, step_def in zip(steps, scenario["steps"]):
        step_type, step_name, step_status = step_details
        assert step_def["type"] == step_type
        assert step_def["text"] == step_name

        for (key, expected) in {
            "passed": StepStatus.passed(step_status),
            "failed": StepStatus.failed(step_status),
            "skipped": StepStatus.skipped(step_status),
        }.items():
            assert step_def.get("stats", {}).get(key, 0) == expected


class TestFeatureRunner(unittest.TestCase):

    def tearDown(self):
        unload_test_data()

    def test_full_pass(self):
        # Given I have Romaine's core
        from romaine.core import Core
        core = Core()
        # And I have some step definitions
        importlib.import_module("test_data.steps.some_steps")
        # And I have a feature object
        steps = (
            ("Given", "step_1", StepStatus.passed),
            ("When", "step_2", StepStatus.passed),
            ("Then", "step_3", StepStatus.passed),
        )
        feature = given_i_have_a_feature_object(steps)
        # When I run the feature
        statistics = core.run_features(feature.copy())
        # Then the output shows that the expected steps have been run
        check_stats(statistics, steps)

    def test_full_fail_then(self):
        # Given I have Romaine's core
        from romaine.core import Core
        core = Core()
        # And I have some step definitions
        importlib.import_module("test_data.steps.some_steps")
        # And I have a feature object
        steps = (
            ("Given", "step_1", StepStatus.passed),
            ("When", "step_2", StepStatus.passed),
            ("Then", "step_8", StepStatus.failed),
        )
        feature = given_i_have_a_feature_object(steps)
        # When I run the feature
        statistics = core.run_features(feature.copy())
        # Then the output shows that the expected steps have been run
        check_stats(statistics, steps)

    def test_full_fail_when(self):
        # Given I have Romaine's core
        from romaine.core import Core
        core = Core()
        # And I have some step definitions
        importlib.import_module("test_data.steps.some_steps")
        # And I have a feature object
        steps = (
            ("Given", "step_1", StepStatus.passed),
            ("When", "step_7", StepStatus.failed),
            ("Then", "step_8", StepStatus.not_reached),
        )
        feature = given_i_have_a_feature_object(steps)
        # When I run the feature
        statistics = core.run_features(feature.copy())
        # Then the output shows that the expected steps have been run
        check_stats(statistics, steps)
