def run_feature(feature, steps, logger):
    with logger.in_feature(feature):
        for scenario in feature["elements"]:
            run_scenario(scenario, steps, logger)


def run_scenario(scenario, steps, logger):
    with logger.in_scenario(scenario):
        step_type = None

        for step in scenario["steps"]:
            if step["type"] in {"Given", "When", "Then"}:
                step_type = step["type"]

            run_step(step, steps, logger, step_type)


def is_valid(step_type, step, last_major):
    if step_type in {step["type"], None}:
        return True
    if step["type"] == "And" and step_type == last_major:
        return True
    return False


def get_match_groups(regex, match):
    key_positions = {k - 1: v for v, k in regex.groupindex}
    args = []
    kwargs = {}
    for i, value in enumerate(match.groups()):
        if i in key_positions:
            key = key_positions[i]
            kwargs[key] = value
        else:
            args.append(value)

    return tuple(args), kwargs


def find_definition(step, steps, step_type):
    step_key = step["text"]
    if step_key in steps:
        return steps[step_key], (), {}

    definitions = sorted(steps.values(), key=lambda d: len(d.name))

    for definition in definitions:
        if not is_valid(definition.prefix, step, step_type):
            continue
        match = definition.regex.match(step_key)
        if match:
            args, kwargs = get_match_groups(definition.regex, match)

            return definition, args, kwargs

    raise NotImplementedError("No step definition for {}"
                              .format(step_key))


def run_step(step, steps, logger, step_type):
    with logger.in_step(step):
        definition, args, kwargs = find_definition(step, steps, step_type)
        definition.func(*args, **kwargs)
