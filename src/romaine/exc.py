# Add Skiptest to exc namespace for more obvious usage
from unittest import SkipTest  # NOQA


class UnimplementedStepError(Exception):
    def __init__(self, step):
        self.step = step
