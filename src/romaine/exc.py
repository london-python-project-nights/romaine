from unittest import SkipTest


class UnimplementedStepError(Exception):
    def __init__(self, step):
        self.step = step
