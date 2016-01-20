

class RomaineLogger(object):

    ERROR = object()

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def alert(self, level, body):
        pass
