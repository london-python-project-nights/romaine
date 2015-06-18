from unittest import TestCase
import importlib


class TestStepFinding(TestCase):

    def test_initial_state(self):
        # Given I have Romaine's core
        from romaine.core import Core
        core = Core()
        # And I have done nothing else
        # Then romaine has no steps
        self.assertFalse(core.steps)

    def test_getting_no_steps(self):
        # Given I have Romaine's core
        from romaine.core import Core
        core = Core()
        # And I get the steps in "steps.no_steps"
        importlib.import_module("tests.steps.no_steps")
        # Then romaine has no steps
        self.assertFalse(core.steps)

    def test_getting_some_steps(self):
        step_names = [
            'step_1',
            'step_2',
            'step_3',
            'step_4',
            'step_5',
        ]
        # Given I have Romaine's core
        from romaine.core import Core
        core = Core()
        # And I get the steps in "steps.some_steps"
        some_steps = importlib.import_module("tests.steps.some_steps")
        # Then romaine has the expected step names
        self.assertEqual(sorted(list(core.steps.keys())), step_names)
        # And romaine has the expected step functions
        for step_name in step_names:
            self.assertEqual(core.steps[step_name].func,
                             getattr(some_steps, step_name))
