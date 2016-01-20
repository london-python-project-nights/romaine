from contextlib import contextmanager

from romaine import exc


def test_step_to_stub(step):

    step_chars = set(step["text"])

    step_slug = "{type}_{text}".format(**step).lower()
    for char in step_chars:
        if not char.isalnum():
            step_slug = step_slug.replace(char, "_")

    return "\n".join([
        "@{type}({text!r})".format(**step),
        "def {step_slug}():".format(step_slug=step_slug),
        "    raise NotImplementedError"
    ])


class RomaineLogger(object):

    INFO = object()
    WARNING = object()
    ERROR = object()

    STEP = object()

    def __init__(self):
        self.current_context = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, exc.UnimplementedStepError):
            self.alert(self.ERROR, (exc_type, exc_val, exc_tb))
            stub = test_step_to_stub(exc_val.step)
            self.alert(self.INFO, stub)
        elif isinstance(exc_val, Exception):
            self.alert(self.ERROR, (exc_type, exc_val, exc_tb))
        else:
            return False
        return True

    @contextmanager
    def in_step(self, step):
        self.current_context = self.STEP, step

        try:
            yield
        except exc.SkipTest:
            self.alert(self.WARNING, "{type} {text} (skipped)".format(**step))
        else:
            self.alert(self.INFO, "{type} {text}".format(**step))

        self.current_context = None

    def alert(self, level, body):
        pass
