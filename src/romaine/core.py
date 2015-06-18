import os


class Core(object):
    """
        The core of the Romaine, provides BDD test API.
    """
    # All located features
    feature_file_paths = []
    instance = None

    def __init__(self):
        """
            Initialise Romaine core.
        """
        self.steps = {}
        Core.instance = self

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

        self.feature_file_paths.extend(feature_candidates)

        return feature_candidates
