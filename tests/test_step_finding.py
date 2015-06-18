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
        expected = {
            'step_1': "Given",
            'step_2': "When",
            'step_3': "Then",
            'step_4': "And",
            'step_5': None,
            'step_6': "Given",
            'step_7': "When",
            'step_8': "Then",
            'step_9': "And",
        }

        step_names = expected.keys()
        # Given I have Romaine's core
        from romaine.core import Core
        core = Core()
        # And I get the steps in "steps.some_steps"
        some_steps = importlib.import_module("tests.steps.some_steps")
        # Then romaine has the expected step names
        self.assertEqual(sorted(list(core.steps.keys())), sorted(step_names))
        # And romaine has the expected step functions
        for step_name in step_names:
            self.assertEqual(core.steps[step_name].func,
                             getattr(some_steps, step_name))
            self.assertEqual(core.steps[step_name].prefix,
                             expected[step_name])
