class SimpleParser(object):
    """
        Gherkin single line parser for Romaine core.
    """
    def is_white(self, line):
        """
            Takes a line and determines whether it is pure whitespace or
            empty.

            Keyword arguments:
            line - Line to test.

            Returns:
            True if the line is purely whitespace or empty. False otherwise.
        """
        return len(line) == 0 or line.isspace()

    def get_tag(self, line):
        """
            Takes a line and gets the tag it contains (if any).

            Keyword arguments:
            line -- Line to seek tag in.

            Returns:
            The tag, or None if none was found.
        """
        line = line.strip()

        disallowed_characters = (' ', '\t', '@')

        if line.startswith('@'):
            line = line.lstrip('@')
            for character in disallowed_characters:
                if character in line:
                    return None
            if len(line) > 0:
                return line
        # If we reach here, no tag was found
        return None

    def is_multiline_delimiter(self, line, closing=False):
        """
            Determines whether the line opens (or closes) a multi-line
            python style string. Per the gherkin spec, only triple " are
            supported, with triple ' not being accepted.

            Also per the BNF-ish gherkin syntax page, a triple " followed by
            anything other than whitespace to end of line will NOT be treated
            as a closing delimiter:
              close_py_string ::= eol space* '\"\"\"' white

            Keyword arguments:
            line - The line to check.
            closing - Whether to check for a closing delimiter. default: False

            Returns:
            True if this is an opening (or closing if requested) delimiter.
            False otherwise.
        """
        line = line.strip()

        if closing:
            if line.endswith('"""'):
                return True
        else:
            if line.startswith('"""'):
                return True

        return False

    def is_comment(self, line):
        """
            Determines whether a given line should be considered to be a
            comment.

            Keyword arguments:
            line - The line to check.

            Returns:
            True if this line is a comment. False otherwise.
        """
        line = line.strip()

        if line.startswith('#'):
            return True

        return False

    def get_cells(self, line):
        """
            Gets cells from the given line if it fits the table structure.
            Cells are divided by | and contain at least one non | character.
            They may be prefixed or suffixed by spaces or tabs.
            They may not contain new lines.

            Keyword arguments:
            line -- THe line to check.

            Returns:
            List of cells found, or None if the line was not valid.
        """
        line = line.strip()

        if line.startswith('|') and line.endswith('|'):
            # Remove leading and trailing pipe
            line = line[1:-1]

            line = line.split('|')

            if '' in line:
                return None

            return line

        return None

    def get_step(self, line):
        """
            Gets step from a given line

            Keyword arguments:
            line -- THe line to check.

            Returns:
            None if the line did not contain a step.
            Otherwise, a dictionary containing:
                type - The step type (e.g. Given)
                text - The text of the step (everything after the keyword)
        """
        line = line.lstrip()
        line = line.split(' ', 1)

        steps = ('Given', 'When', 'Then', 'And', 'But')

        for step in steps:
            if line[0] == step:
                return {
                    'type': step,
                    'text': line[1],
                }

        return None

    def get_section_start(self, line):
        """
            Determines whether a line starts a Background, Scenario, Examples,
            or Scenario Outline section.

            Keyword arguments:
            line - The line to check.

            Returns:
            The lowercase section type (e.g. 'examples') if this line starts a
            section. None otherwise.
        """
        line = line.lstrip()

        section_type = None
        description = None

        sections = {
            'Examples:': 'examples',
            'Background:': 'background',
            'Scenario:': 'scenario',
            'Scenario Outline:': 'scenario outline',
        }

        for section, section_type_candidate in sections.items():
            if line.startswith(section):
                section_type = section_type_candidate
                description = line.split(':', 1)[1]
                break

        return {
            'type': section_type,
            'description': description,
        }
