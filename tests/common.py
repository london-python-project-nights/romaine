import json
import os
import sys

# Allow the tests to work from a tests subdir, then import the test target
test_path = os.path.dirname(__file__)
package_directory = os.path.join(os.path.split(test_path)[0], 'src')
sys.path.append(package_directory)

PARSER_TEST_DATA_DIR = os.path.join(
    os.path.split(test_path)[0],
    'test_data',
    'parser',
)

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


def get_parser_input(target):
    """
        Get input data as a list for the parser.
    """
    input_path = os.path.join(PARSER_TEST_DATA_DIR, target)
    with open(input_path) as input_handle:
        data = input_handle.read().splitlines()

    return data


def get_parser_output(target):
    """
        Get expected output for given input.
    """
    output_path = os.path.join(PARSER_TEST_DATA_DIR, target)
    with open(output_path) as output_handle:
        data = json.load(output_handle)
    return data
