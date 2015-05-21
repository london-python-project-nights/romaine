import nose
import importlib


def test_initial_state():
    # Given I have Romaine's core
    from romaine.core import Core
    core = Core()
    # And I have done nothing else
    # Then romaine has no steps
    nose.tools.assert_false(core.steps)


def test_getting_no_steps():
    # Given I have Romaine's core
    from romaine.core import Core
    core = Core()
    # And I get the steps in "steps.no_steps"
    importlib.import_module("steps.no_steps", package=".")
    # Then romaine has no steps
    nose.tools.assert_false(core.steps)


def test_getting_some_steps():
    # Given I have Romaine's core
    from romaine.core import Core
    core = Core()
    # And I get the steps in "steps.some_steps"
    importlib.import_module("steps.some_steps", package=".")
    # Then romaine has no steps
    nose.tools.assert_equal(core.steps,
                            [
                                'step_1',
                                'step_2',
                                'step_3',
                                'step_4',
                                'step_5',
                            ])
