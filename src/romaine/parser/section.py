from romaine.parser.exceptions import (
    MalformedTableError,
)
from copy import copy


class SectionParser(object):
    """
        Gherkin section parser for Romaine core.
        This is intended to handle Examples, Background, Scenario, and
        Scenario Outlines.
    """
    def __init__(self, simple_parser, multiline_parser, step_parser):
        """
            Initialise section parser.

            Keyword arguments:
            simple_parser - An instance of a simple parser.
            multiline_parser - An instance of a multiline parser.
        """
        self.simple = simple_parser
        self.multiline = multiline_parser
        self.step = step_parser

    def get_example(self, lines):
        """
            Takes a set of lines and attempts to retrieve an Examples section
            from them.

            Keyword arguments:
            lines - list of lines to consume.

            Returns:
            A dict containing:
                example - None if none found, otherwise a dict containing:
                    description - The description of the examples
                    columns - A dict containing:
                        each column name: [list of this column]
                remaining - Any lines not consumed by this function
                raw_input - The input data for this function
        """
        lines = copy(lines)
        results = {
            'example': None,
            'remaining': [],
            'raw_input': copy(lines),
        }

        # Get leading comments and whitespace
        comments = self.multiline.get_comments_with_space(lines)
        leading_comments_and_space = comments['comments_and_space']
        lines = comments['remaining']

        if len(lines) > 0:
            section_start = self.simple.get_section_start(lines[0])
        else:
            section_start = {'type': None}

        if section_start['type'] == 'examples':
            description = section_start['description']

            section_start_line = lines[0]
            lines = lines[1:]

            table = self.multiline.get_table(lines)

            if table['table'] is not None:
                lines = table['remaining']
                table = table['table']

                # Get the table with column headings
                columns = {}
                for position, header in enumerate(table[0]):
                    try:
                        # Get the same column from each following row
                        column = [item[position] for item in table[1:]]
                    except IndexError:
                        raise MalformedTableError(
                            'Each row in an Examples table must have the same '
                            'number of columns.'
                        )

                    columns[header] = column

                space = self.multiline.get_space(lines)
                trailing_space = space['space']
                lines = space['remaining']

                results['example'] = {
                    'description': description,
                    'columns': columns,
                    'table': table,
                    'leading_comments_and_space': leading_comments_and_space,
                    'trailing_whitespace': trailing_space,
                }

        if results['example'] is None:
            if section_start['type'] == 'examples':
                start = leading_comments_and_space + [section_start_line]
            else:
                start = leading_comments_and_space
            lines = start + lines

        results['remaining'] = lines

        return results

    def get_examples(self, lines):
        """
            Takes a set of lines and attempts to retrieve Examples sections
            until there are no more valid examples sections at the start of
            the remaining input lines.

            Keyword arguments:
            lines - list of lines to consume.

            Returns:
            A dict containing:
                examples - A list of examples sections found using get_example
                           until no example is found.
                remaining - Any lines not consumed by this function
                raw_input - The input data for this function
        """
        original_lines = copy(lines)
        lines = copy(lines)

        examples = []

        finished = False
        while not finished:
            next_example = self.get_example(lines)
            lines = next_example['remaining']
            if next_example['example'] is None:
                finished = True
            else:
                examples.append(next_example['example'])

        return {
            'examples': examples,
            'remaining': lines,
            'raw_input': original_lines,
        }

    def get_element(self, lines):
        """
            Takes a set of lines and attempts to retrieve Scenarios or
            Scenario Outlines from them. Named elements due to the bnf-ish
            Gherkin syntax from Gherkin's repo.

            Keyword arguments:
            lines - list of lines to consume.

            Returns:
            A dict containing:
                element - None if no scenarios or outlines found.
                          Otherwise, a dict containing:
                    type - The element type: 'scenario' or 'scenario outline'
                    leading_comments_and_space - Leading comments and space
                    tags - Any leading tags
                    description - The description of this scenario/outline,
                                  this being anything following the keyword
                                  and colon.
                                  e.g. Scenario: This is the description.
                    steps - A list of steps as retrieved by get_steps
                remaining - Any lines not consumed by this function
                raw_input - The input data for this function
        """
        original_lines = lines
        lines = copy(lines)

        comments = self.multiline.get_comments_with_space(lines)
        lines = comments['remaining']
        leading_comments_and_space = comments['comments_and_space']

        tags = self.multiline.get_tags(lines)
        lines = tags['remaining']
        tags = tags['tags']

        if len(lines) > 0:
            section = self.simple.get_section_start(lines[0])
            element_type = section['type']
            description = section['description']
        else:
            element_type = None

        lines = lines[1:]

        if element_type in ('scenario', 'scenario outline'):
            steps = self.step.get_steps(lines)
            lines = steps['remaining']
            steps = steps['steps']

            element = {
                'leading_comments_and_space': leading_comments_and_space,
                'type': element_type,
                'tags': tags,
                'description': description,
                'steps': steps,
            }
        else:
            element = None
            remaining = original_lines

        if element_type == 'scenario outline':
            examples = self.get_examples(lines)
            lines = examples['remaining']
            element['examples'] = examples['examples']

        if element is not None:
            remaining = lines

        return {
            'element': element,
            'remaining': remaining,
            'raw_input': original_lines,
        }

    def get_elements(self, lines):
        """
            Takes a set of lines and attempts to retrieve Scenarios or
            Scenario Outlines from them until none of these elements
            remain at the beginning of the remaining lines of input.

            Keyword arguments:
            lines - list of lines to consume.

            Returns:
            A dict containing:
                elements - A list of Scenarios or Scenario Outlines as
                           retrieved by calls to get_element.
                remaining - Any lines not consumed by this function
                raw_input - The input data for this function
        """
        lines = copy(lines)
        original_lines = copy(lines)
        elements = []

        finished = False
        while not finished:
            element = self.get_element(lines)
            if element['element'] is not None:
                elements.append(element['element'])
                lines = element['remaining']
            else:
                finished = True

        return {
            'elements': elements,
            'remaining': lines,
            'raw_input': original_lines,
        }

    def get_background(self, lines):
        """
            Takes a set of lines and attempts to retrieve a Background section
            from them.

            Keyword arguments:
            lines - list of lines to consume.

            Returns:
            A dict containing:
                example - None if none found, otherwise a dict containing:
                    leading_comments_and_space - Leading comments and space
                    description - The description of the background
                    steps - A list of steps as retrieved by get_steps
                remaining - Any lines not consumed by this function
                raw_input - The input data for this function
        """
        lines = copy(lines)
        results = {
            'background': None,
            'remaining': [],
            'raw_input': copy(lines),
        }

        # Get leading comments and whitespace
        comments = self.multiline.get_comments_with_space(lines)
        leading_comments_and_space = comments['comments_and_space']
        lines = comments['remaining']

        if len(lines) > 0:
            section_start = self.simple.get_section_start(lines[0])
        else:
            section_start = {'type': None}

        if section_start['type'] == 'background':
            description = section_start['description']

            lines = lines[1:]

            steps = self.step.get_steps(lines)
            lines = steps['remaining']
            steps = steps['steps']

            results['background'] = {
                'description': description,
                'steps': steps,
                'leading_comments_and_space': leading_comments_and_space,
            }

        if results['background'] is None:
            start = leading_comments_and_space
            lines = start + lines

        results['remaining'] = lines

        return results

    def get_header(self, lines):
        """
            Takes a set of lines and retrieves the header from the beginning.
            The header is all lines until a background, scenario, or scenario
            outline is found.

            Keyword arguments:
            lines - list of lines to consume.

            Returns:
            A dict containing:
                header - List of lines until first element or background is
                         found.
                remaining - Any lines not consumed by this function
                raw_input - The input data for this function
        """
        lines = copy(lines)
        original_lines = copy(lines)
        header = []

        finished = False
        while not finished:
            element = self.get_element(lines)['element']
            background = self.get_background(lines)['background']

            if element is None and background is None and len(lines) > 0:
                header.append(lines[0])
                lines = lines[1:]
            else:
                finished = True

        return {
            'header': header,
            'remaining': lines,
            'raw_input': original_lines,
        }
