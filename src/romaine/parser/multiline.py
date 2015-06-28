from romaine.parser.exceptions import UnclosedPythonishString
from copy import copy


class MultilineParser(object):
    """
        Gherkin multi-line parser for Romaine core.
    """
    def __init__(self, simple_parser):
        """
            Initialise multi-line parser.

            Keyword arguments:
            simple_parser - An instance of a simple parser.
        """
        self.simple = simple_parser

    def get_pythonish_string(self, lines):
        """
            Takes a set of lines and attempts to retrieve the pythonish string
            they start with.

            Keyword arguments:
            lines - list of lines to consume.

            Returns:
            Dict containing:
              pythonish_string - list of lines in pythonish string or None
              remaining - lines remaining after pythonish string is consumed
        """
        lines = copy(lines)
        original_lines = copy(lines)
        result = []

        if self.simple.is_multiline_delimiter(lines[0]):
            # Reverse the lines for easier sequential processing
            lines.reverse()

            # Make sure we have any applicable parts of the first line
            first_line = lines.pop()
            first_line = first_line.lstrip()
            first_line = first_line[3:]
            result.append(first_line)

            if len(lines) == 0:
                raise UnclosedPythonishString(
                    'Input terminated by start of unclosed multiline string '
                    '(""").'
                )
            next_line = lines.pop()

            while not self.simple.is_multiline_delimiter(next_line,
                                                         closing=True):
                result.append(next_line)
                if len(lines) == 0:
                    raise UnclosedPythonishString(
                        'Unexpected end of input when searching for multiline'
                        ' string terminator (""").'
                    )
                next_line = lines.pop()

            # Get rid of the delimiter before adding the last line
            next_line = next_line.rstrip()
            next_line = next_line[:-3]
            result.append(next_line)

            # Fix the line ordering
            lines.reverse()

        if result == []:
            result = None

        return {
            'pythonish_string': result,
            'remaining': lines,
            'raw_input': original_lines,
        }

    def get_table(self, lines):
        """
            Takes a set of lines and attempts to retrieve a table from the
            start of those lines.

            Keyword arguments:
            lines - list of lines to consume.

            Returns:
            Dict containing:
              table - list of rows in table or None
              remaining - lines remaining after table is consumed
        """
        lines = copy(lines)
        original_lines = copy(lines)
        result = []

        if lines[0].startswith('|'):
            # Reverse the lines for easier sequential processing
            lines.reverse()

            next_line = lines.pop()
            next_cells = self.simple.get_cells(next_line)

            while next_cells is not None:
                result.append(next_cells)
                # Check whether there are any lines remaining to process
                if len(lines) > 0:
                    next_line = lines.pop()
                    next_cells = self.simple.get_cells(next_line)
                else:
                    break

            # The input still contains items which are not part of a table,
            # let's not lose them
            if next_cells is None:
                lines.append(next_line)

            # Fix the line ordering
            lines.reverse()

        if result == []:
            result = None

        return {
            'table': result,
            'remaining': lines,
            'raw_input': original_lines,
        }

    def get_multiline_arg(self, lines):
        """
            Takes a set of lines and attempts to retrieve a table or pythonish
            string from the start of those lines.

            Keyword arguments:
            lines - list of lines to consume.

            Returns:
            Dict containing:
              type - table or multiline_string if either of those was found.
                     None if neither was found.
              data - pythonish string list or list of lists of cells in table;
                     None if no multiline arg was found.
              remaining - lines remaining after multiline arg is consumed
        """
        lines = copy(lines)
        original_lines = copy(lines)
        table = self.get_table(lines)
        if table['table'] is not None:
            result = table['table']
            remaining = table['remaining']
            arg_type = 'table'
        else:
            pythonish_string = self.get_pythonish_string(lines)
            if pythonish_string['pythonish_string'] is not None:
                result = pythonish_string['pythonish_string']
                remaining = pythonish_string['remaining']
                arg_type = 'multiline_string'
            else:
                result = None
                remaining = lines
                arg_type = None

        return {
            'type': arg_type,
            'data': result,
            'remaining': remaining,
            'raw_input': original_lines,
        }

    def get_comments_with_space(self, lines):
        """
            Takes a set of lines and attempts to get leading comments with
            whitespace from them. They must start with a comment.

            Keyword arguments:
            lines - list of lines to consume.

            Returns:
            A dict containing:
                comments_and_space - List of comments or empty lines
                                     (including whitespace).
                remaining - Any lines not consumed by this function
        """
        lines = copy(lines)
        original_lines = copy(lines)
        results = {
            'comments_and_space': [],
            'remaining': [],
            'raw_input': original_lines,
        }

        # We must start with a comment
        if len(lines) > 0 and self.simple.is_comment(lines[0]):
            lines.reverse()
            finished = False
            while len(lines) > 0 and not finished:
                next_line = lines.pop()
                if self.simple.is_white(next_line) or \
                   self.simple.is_comment(next_line):
                    results['comments_and_space'].append(next_line)
                else:
                    # This wasn't whitespace or a comment, put it back on the
                    # list of lines
                    lines.append(next_line)
                    finished = True

            lines.reverse()

        results['remaining'] = lines

        return results

    def get_space(self, lines):
        """
            Takes a set of lines and gets all blank lines or lines containing
            only whitespace until the first non blank/whitespace line is
            reached.

            Keyword arguments:
            lines - list of lines to consume.
            Returns:
            A dict containing:
                space - The leading whitespace/blank lines
                remaining - Any lines not consumed by this function
        """
        lines = copy(lines)
        original_lines = copy(lines)
        results = {
            'space': [],
            'remaining': [],
            'raw_input': original_lines,
        }

        lines.reverse()

        while len(lines) > 0:
            next_line = lines.pop()
            if self.simple.is_white(next_line):
                results['space'].append(next_line)
            else:
                results['remaining'].append(next_line)
                break

        lines.reverse()
        results['remaining'].extend(lines)

        return results

    def get_tags(self, lines):
        """
            Takes a set of lines and attempts to get tags from the lines.
            There may be spaces or blank lines between or after the tags,
            but all such whitespace will be discarded.
            The lines must start with a tag for any tags to be retrieved.

            Keyword arguments:
            lines - list of lines to consume.

            Returns:
            A dict containing:
                tags - A list of tags found.
                remaining - Any lines not consumed by this function
        """
        lines = copy(lines)
        original_lines = copy(lines)
        results = {
            'tags': [],
            'remaining': [],
            'raw_input': original_lines,
        }

        lines.reverse()

        while len(lines) > 0:
            next_line = lines.pop()
            tag = self.simple.get_tag(next_line)

            if tag is not None:
                results['tags'].append(tag)
            elif len(results['tags']) == 0:
                # The first line isn't a tag, abort.
                lines.append(next_line)
                break
            elif self.simple.is_white(next_line):
                # Line must be whitespace, discard it and continue
                pass
            else:
                # The line isn't a tag, we're finished.
                lines.append(next_line)
                break

        lines.reverse()
        results['remaining'].extend(lines)

        return results
