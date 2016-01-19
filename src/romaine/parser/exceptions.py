class UnclosedPythonishString(Exception):
    """
        Exception for pythonish strings that have not been closed correctly.
    """
    pass


class MalformedTableError(Exception):
    """
        Invalid table in examples section.
    """
    pass


class FeatureTrailingDataError(Exception):
    """
        Feature has trailing data.
    """
    pass
