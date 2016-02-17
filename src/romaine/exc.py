# Add Skiptest to exc namespace for more obvious usage
# noinspection PyUnresolvedReferences
from unittest import SkipTest


class UnimplementedStepError(Exception):
    def __init__(self, step):
        self.step = step
