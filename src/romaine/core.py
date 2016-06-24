import os
import logging

from romaine.logs import RomaineLogger
from romaine.parser import Parser
from romaine import runner


class Core(object):
    """
        The core of the Romaine, provides BDD test API.
    """
    # All located features
    feature_file_paths = set()
    instance = None

    def __init__(self, log_level=logging.WARNING):
        """
            Initialise Romaine core.
        """
        self.steps = {}
        self.Parser = Parser
        Core.instance = self
        self.log_level = log_level

    def locate_features(self, path):
        """
            Locate any features given a path.

            Keyword arguments:
            path -- The path to search for features, recursively.

            Returns:
            List of features located in the path given.
        """
        walked_paths = os.walk(path)

        # Features in this path are stored in an intermediate list before
        # being added to the class variable so that we can return only the
        # ones we find on this invocation of locate_features
        feature_candidates = []

        for walked_path in walked_paths:
            base_directory, sub_directories, feature_files = walked_path
            for feature_file in feature_files:
                feature_candidates.append(
                    os.path.join(
                        base_directory,
                        feature_file
                    )
                )

        self.feature_file_paths.update(feature_candidates)

        return feature_candidates

    def run_features(self, *features):
        with RomaineLogger(out_level=self.log_level) as logger:
            r = runner.Runner(logger, self.steps)
            for feature in features:
                r.feature(feature)
        return logger.statistics
