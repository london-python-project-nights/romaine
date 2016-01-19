from romaine.parser import (
    simple,
    multiline,
    step,
    section,
    feature,
)
from romaine.parser.exceptions import (  # noqa
    UnclosedPythonishString,
    MalformedTableError,
)


class Parser(object):
    """
        Gherkin parser for romaine core.
    """

    def __init__(self):
        """
            Initialise a Gherkin parser.
        """
        self.simple = simple.SimpleParser()
        self.multiline = multiline.MultilineParser(self.simple)
        self.step = step.StepParser(self.simple, self.multiline)
        self.section = section.SectionParser(
            self.simple,
            self.multiline,
            self.step,
        )
        self.feature = feature.FeatureParser(
            self.multiline,
            self.section,
        )
