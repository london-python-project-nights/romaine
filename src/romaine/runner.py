def run_feature(feature, steps, logger):
    with logger.in_feature(feature):
        for scenario in feature["elements"]:
            run_scenario(scenario, steps, logger)


def run_scenario(scenario, steps, logger):
    with logger.in_scenario(scenario):
        for step in scenario["steps"]:
            run_step(step, steps, logger)


def run_step(step, steps, logger):
    with logger.in_step(step):
        pass
