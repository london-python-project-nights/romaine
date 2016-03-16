import os
import sys

# Allow the tests to work from a tests subdir, then import the test target
test_path = os.path.dirname(__file__)
package_directory = os.path.join(os.path.split(test_path)[0], 'src')
sys.path.append(package_directory)

# Module to be tested
import romaine


def unload_test_data():
    keys = tuple(
        key for key in sys.modules
        if key.startswith("test_data")
    )
    for key in keys:
        sys.modules.pop(key)


# Utility for getting an initialised parser.
def get_romaine_parser():
    return romaine.Core().Parser()
