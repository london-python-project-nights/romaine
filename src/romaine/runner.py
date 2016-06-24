import re


VARIABLE = re.compile("<([^><\n]+)>")


class ExampleTable(object):
    def add_hashes(self):
        rows = self.table["table"]
        rows = [list(map(str.strip, row)) for row in rows]
        self.header = rows[0]
        self.rows = [row for row in rows[1:] if row]
        self.hashes = self.table["hashes"] = []

        for row in self.rows:
            if len(row) != len(self.header):
                raise IndexError(
                    "Row {} must be the same length as heading {}"
                    .format(row, self.header)
                )
            self.hashes.append(dict(zip(self.header, row)))

    def __init__(self, table):
        self.table = table
        self.add_hashes()

        self.header = None
        self.rows = None
        self.hashes = None

    def filled(self, steps):
        for i, data in enumerate(self.hashes, start=1):
            string = self.table["table"][i]
            row = ExampleRow(string, data)
            yield string, row.apply_steps(steps)


class ExampleRow(object):
    def __init__(self, string, data):
        self.string = string
        self.data = data

    def apply_steps(self, steps):
        return list(map(self.apply_step, steps))

    def apply_step(self, step):
        return Variable.apply_all(step, self.data)


class Variable(object):
    pattern = re.compile("<([^><\n]+)>")

    @classmethod
    def apply_all(cls, step, example_row):
        step = step.copy()
        for var in cls.pattern.findall(step["text"]):
            example = example_row[var]
            cls(example, var).apply_on(step)
        return step

    def __init__(self, example, variable):
        self.example = example
        self.variable = variable
        self.formatted = "<{}>".format(variable)

    def _replaced(self, string):
        return string.replace(self.formatted, self.example)

    def apply_on(self, step):
        step["text"] = self._replaced(step["text"])
        step["raw"] = list(map(self._replaced, step["raw"]))


class Runner(object):
    def __init__(self, logger, step_definitions):
        self.logger = logger
        self.step_definitions = step_definitions

    def feature(self, feature):
        with self.logger.in_feature(feature):
            for scenario in feature["elements"]:
                handlers = {
                    "scenario": self.scenario,
                    "scenario outline": self.scenario_outline,
                }
                key = scenario["type"]
                handlers[key](scenario)

    def scenario(self, scenario):
        with self.logger.in_scenario(scenario):
            step_type = None

            for step in scenario["steps"]:
                if step["type"] in {"Given", "When", "Then"}:
                    step_type = step["type"]

                self.step(step, step_type)

    def scenario_outline(self, scenario):
        with self.logger.in_scenario_outline(scenario):
            for table in map(ExampleTable, scenario["examples"]):
                table.add_hashes()
                with self.logger.in_scenario_outline_example(table.table):
                    outline_steps = scenario["steps"]
                    for string, filled_steps in table.filled(outline_steps):
                        self.scenario_outline_row(string, filled_steps)

    def scenario_outline_row(self, string, filled_steps):
        with self.logger.in_scenario_outline_example_row(string, filled_steps):
            step_type = None

            for step in filled_steps:
                if step["type"] in {"Given", "When", "Then"}:
                    step_type = step["type"]

                self.step(step, step_type)

    def find_definition(self, step, step_type):
        steps = self.step_definitions
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

    def step(self, step, step_type):
        with self.logger.in_step(step):
            definition, args, kwargs = self.find_definition(step, step_type)
            definition.func(*args, **kwargs)


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
    definition, args, kwargs = find_definition(step, steps, step_type)
    definition.func(*args, **kwargs)
