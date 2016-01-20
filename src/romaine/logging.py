

class RomaineLogger(object):

    INFO = object()
    WARNING = object()
    ERROR = object()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, Exception):
            self.alert(self.INFO, exc_val)
            self.alert(self.ERROR, exc_val)
            return True

    def alert(self, level, body):
        pass
