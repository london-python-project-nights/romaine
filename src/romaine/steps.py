from romaine.core import Core


class Step(object):
    def __init__(self, name):
        self.name = name
        self.func = None

    def __call__(self, func):
        self.func = func
        Core.instance.steps[self.name] = self
        return func


class Given(Step):
    pass


class When(Step):
    pass


class Then(Step):
    pass


class And(Step):
    pass
