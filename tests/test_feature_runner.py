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
        'raw': ["  Given {}".format(text)],
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
    steps_total = 0
    steps_passed = 0
    steps_skipped = 0
    steps_failed = 0

    all_passed = None
    all_failed = False

    for (_, __, status) in steps:
        steps_total += 1
        if StepStatus.passed(status):
            steps_passed += 1
            if all_passed is None:
                all_passed = True
        elif StepStatus.skipped(status):
            steps_skipped += 1
        elif StepStatus.failed(status):
            steps_failed += 1
            all_failed = True
            all_passed = False

    if all_passed is None:
        all_passed = False

    features_total = scenarios_total = 1
    features_passed = scenarios_passed = 1 if all_passed else 0
    scenarios_failed = scenarios_total - scenarios_passed

    assert statistics["scenarios"]["total"] == scenarios_total
    assert statistics["scenarios"]["passed"] == scenarios_passed

    assert statistics["steps"]["total"] == steps_total
    assert statistics["steps"]["passed"] == steps_passed
    assert statistics["steps"]["skipped"] == steps_skipped
    assert statistics["steps"]["failed"] == steps_failed

    assert statistics["features"]["total"] == features_total
    assert statistics["features"]["passed"] == features_passed

    assert len(statistics["features"]["run"]) == 1
    feature = statistics["features"]["run"][0]
    feature_stats = feature["stats"]

    assert feature_stats["passed_steps"] == steps_passed
    assert feature_stats["failed_steps"] == steps_failed
    assert feature_stats["skipped_steps"] == steps_skipped
    assert feature_stats["total_steps"] == steps_total
    assert feature_stats["passed_scenarios"] == scenarios_passed
    assert feature_stats["failed_scenarios"] == scenarios_failed
    assert feature_stats["total_scenarios"] == scenarios_total
    assert feature_stats["passed"] == all_passed
    assert feature_stats["failed"] == all_failed

    assert len(feature["elements"]) == 1
    scenario = feature["elements"][0]
    scenario_stats = scenario["stats"]

    assert scenario_stats["passed_steps"] == steps_passed
    assert scenario_stats["failed_steps"] == steps_failed
    assert scenario_stats["skipped_steps"] == steps_skipped
    assert scenario_stats["total_steps"] == steps_total
    assert scenario_stats["passed"] == all_passed
    assert scenario_stats["failed"] == all_failed

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
        # And I have a feature with one scenario of the following steps:
        #   | step_type | step_text | step_status   |
        #   | Given     | step_1    | passed        |
        #   | When      | step_2    | passed        |
        #   | Then      | step_3    | passed        |
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
        # And I have a feature with one scenario of the following steps:
        #   | step_type | step_text | step_status   |
        #   | Given     | step_1    | passed        |
        #   | When      | step_2    | passed        |
        #   | Then      | step_8    | failed        |
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
        # And I have a feature with one scenario of the following steps:
        #   | step_type | step_text | step_status   |
        #   | Given     | step_1    | passed        |
        #   | When      | step_7    | failed        |
        #   | Then      | step_8    | not reached   |
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

    def test_full_skip_last(self):
        # Given I have Romaine's core
        from romaine.core import Core
        core = Core()
        # And I have some step definitions
        importlib.import_module("test_data.steps.some_steps")
        # And I have a feature with one scenario of the following steps:
        #   | step_type | step_text | step_status   |
        #   | Given     | step_1    | passed        |
        #   | When      | step_2    | passed        |
        #   | Then      | step_3    | passed        |
        #   | And       | step_9    | skipped       |
        steps = (
            ("Given", "step_1", StepStatus.passed),
            ("When", "step_2", StepStatus.passed),
            ("Then", "step_3", StepStatus.passed),
            ("And", "step_9", StepStatus.skipped),
        )
        feature = given_i_have_a_feature_object(steps)
        # When I run the feature
        statistics = core.run_features(feature.copy())
        # Then the output shows that the expected steps have been run
        check_stats(statistics, steps)

    def test_full_skip_second(self):
        # Given I have Romaine's core
        from romaine.core import Core
        core = Core()
        # And I have some step definitions
        importlib.import_module("test_data.steps.some_steps")
        # And I have a feature with one scenario of the following steps:
        #   | step_type | step_text | step_status   |
        #   | Given     | step_1    | passed        |
        #   | And       | step_9    | skipped       |
        #   | When      | step_2    | not reached   |
        #   | Then      | step_3    | not reached   |
        steps = (
            ("Given", "step_1", StepStatus.passed),
            ("And", "step_9", StepStatus.skipped),
            ("When", "step_2", StepStatus.not_reached),
            ("Then", "step_3", StepStatus.not_reached),
        )
        feature = given_i_have_a_feature_object(steps)
        # When I run the feature
        statistics = core.run_features(feature.copy())
        # Then the output shows that the expected steps have been run
        check_stats(statistics, steps)

    # def test_regex_steps(self):
    #     # Given I have Romaine's core
    #     from romaine.core import Core
    #     core = Core()
    #     # And I have some step definitions
    #     importlib.import_module("test_data.steps.regex_steps")
    #     # And I have a feature with one scenario of the following steps:
    #     #   | step_type | step_text | step_status   |
    #     #   | Given     | step_1    | passed        |
    #     #   | When      | step_2    | not reached   |
    #     #   | Then      | step_3    | not reached   |
    #     steps = (
    #         ("Given", "step_1", StepStatus.passed),
    #         ("When", "step_2", StepStatus.passed),
    #         ("Then", "step_3", StepStatus.passed),
    #     )
    #     feature = given_i_have_a_feature_object(steps)
    #     # When I run the feature
    #     statistics = core.run_features(feature.copy())
    #     # Then the output shows that the expected steps have been run
    #     check_stats(statistics, steps)
