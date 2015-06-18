from romaine.core import Core


class Step(object):
    prefix = None

    def __init__(self, name):
        self._raw_name = name
        if self.prefix is not None and name.startswith(self.prefix):
            # Was complaining about len(None) - we have guarded against this
            # noinspection PyTypeChecker
            name = name[len(self.prefix)+1:]
        self.name = name.strip()
        self.func = None

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
