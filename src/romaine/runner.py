def run_feature(feature, steps, logger):
    with logger.in_feature(feature):
        for scenario in feature["elements"]:
            run_scenario(scenario, steps, logger)


def run_scenario(scenario, steps, logger):
    with logger.in_scenario(scenario):
        for step in scenario["steps"]:
            run_step(step, steps, logger)


def find_definition(step, steps):
    step_key = step["text"]
    return steps[step_key]


def run_step(step, steps, logger):
    with logger.in_step(step):
        find_definition(step, steps).func()
