class Core(object):
    instance = None

    def __init__(self):
        self.steps = {}
        Core.instance = self
