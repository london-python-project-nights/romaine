import re

from romaine.core import Core


class Step(object):
    prefix = None

    def __init__(self, name):
        self._raw_name = name

        if self.prefix is not None:
            prefix = self.prefix + " "
            if name.startswith(prefix):
                name = name[len(prefix):]
        self.name = name.strip()
        self.func = None
        self.regex = re.compile(self.name)

    def __call__(self, func):
        self.func = func
        Core.instance.steps[self.name] = self
        return func


class Given(Step):
    prefix = "Given"
    pass


class When(Step):
    prefix = "When"
    pass


class Then(Step):
    prefix = "Then"
    pass


class And(Step):
    prefix = "And"
    pass
