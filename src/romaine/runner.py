import re


VARIABLE = re.compile("<([^><\n]+)>")


def run_feature(feature, steps, logger):
    with logger.in_feature(feature):
        for scenario in feature["elements"]:
            handlers = {
                "scenario": run_scenario,
                "scenario outline": run_scenario_outline,
            }
            key = scenario["type"]

            handlers[key](scenario, steps, logger)


def run_scenario(scenario, steps, logger):
    with logger.in_scenario(scenario):
        step_type = None

        for step in scenario["steps"]:
            if step["type"] in {"Given", "When", "Then"}:
                step_type = step["type"]

            run_step(step, steps, logger, step_type)


class Rows(object):
    def __init__(self, rows):
        rows = [list(map(str.strip, row)) for row in rows]
        self.header = rows[0]
        self.rows = rows[1:]

    def __iter__(self):
        for row in self.rows:
            if not row:
                continue

            if len(row) != len(self.header):
                raise IndexError(
                    "Row {} must be the same length as heading {}"
                    .format(row, self.header)
                )
            yield dict(zip(self.header, row))

    @property
    def as_list(self):
        return list(self)


def run_scenario_outline(scenario, steps, logger):
    with logger.in_scenario_outline(scenario):
        for table in scenario["examples"]:
            table["hashes"] = Rows(table["table"]).as_list

            with logger.in_scenario_outline_example(table):
                for i, row in enumerate(table["hashes"]):

                    with logger.in_scenario_outline_example_row(table, i):
                        run_scenario_outline_row(scenario, steps, logger, row)


def run_scenario_outline_row(scenario, steps, logger, row):
    step_type = None

    for step in scenario["steps"]:
        if step["type"] in {"Given", "When", "Then"}:
            step_type = step["type"]

        variables = VARIABLE.findall(step["text"])

        step = step.copy()
        for variable in variables:
            replaced = lambda x: x.replace(
                "<{}>".format(variable),
                row[variable],
            )
            step["text"] = replaced(step["text"])
            step["raw"] = [replaced(part) for part in step["raw"]]

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
