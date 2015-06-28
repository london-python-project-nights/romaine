from copy import copy


class StepParser(object):
    """
        Gherkin step parser for Romaine core.
    """
    def __init__(self, simple_parser, multiline_parser):
        """
            Initialise step parser.

            Keyword arguments:
            simple_parser - An instance of a simple parser.
            multiline_parser - An instance of a multiline parser.
        """
        self.simple = simple_parser
        self.multiline = multiline_parser

    def get_step(self, lines):
        """
            Takes a list of lines and attempts to extract a single step from
            them.

            Keyword arguments:
            lines -- The lines to seek a step in.

            Returns:
            Dict containing:
                step -- None if no step was found.
                        Otherwise, dict containing:
                    leading_comments_and_space -- Any preceding
                                                  comments and
                                                  whitespace or None.
                    type -- The type of step found
                    text -- The text of the step
                    multiline_arg -- Any multiline arg directly following the
                                     step, containing type and data per
                                     get_multiline_arg.
                                     None if no multiline arg present.
                    trailing_whitespace -- Any trailing whitespace.
                remaining -- List of remaining lines after one step has been
                             consumed.
                raw_input - The input data for this function
        """
        # TODO: Line reversing logic in this function is hideous. Fix it.
        lines = copy(lines)
        original_lines = copy(lines)

        step = None

        # Get leading comments and whitespace
        comments = self.multiline.get_comments_with_space(lines)
        leading_comments_and_space = comments['comments_and_space']
        lines = comments['remaining']

        # Reverse line ordering for ease of processing with pop
        lines.reverse()

        # Now get the step
        step_line = None
        if len(lines) > 0:
            step_line = lines.pop()
            step = self.simple.get_step(step_line)

        if step is None:
            if step_line is not None:
                lines.append(step_line)
            # Keep any leading comments and space
            lines = leading_comments_and_space + lines
        else:
            # Get multiline argument if applicable, then any trailing space
            multiline_arg = None
            trailing_whitespace = []
            if len(lines) > 0:
                # For this, lines must be in the right order
                lines.reverse()
                multiline = self.multiline.get_multiline_arg(lines)
                if multiline['type'] is not None:
                    multiline_arg = {
                        'type': multiline['type'],
                        'data': multiline['data'],
                    }
                lines = multiline['remaining']

                # Get whitespace
                space = self.multiline.get_space(lines)
                trailing_whitespace = space['space']
                lines = space['remaining']

                # For final steps, lines must be reversed again
                lines.reverse()

            step = {
                'leading_comments_and_space': leading_comments_and_space,
                'type': step['type'],
                'text': step['text'],
                'multiline_arg': multiline_arg,
                'trailing_whitespace': trailing_whitespace,
            }

        # Fix line ordering
        lines.reverse()

        return {
            'step': step,
            'remaining': lines,
            'raw_input': original_lines,
        }

    def get_steps(self, lines):
        """
            Takes a set of lines and attempts to retrieve sequential steps
            from the start of the set of lines.

            Keyword arguments:
            lines - list of lines to consume.

            Returns:
            Dict containing:
                steps - list of steps as returned by get_step
                remaining - lines remaining after steps are consumed
                raw_input - The input data for this function
        """
        lines = copy(lines)
        original_lines = copy(lines)
        steps = []
        finished_finding_steps = False
        while not finished_finding_steps:
            step = self.get_step(lines)
            if step['step'] is not None:
                steps.append(step['step'])
                lines = step['remaining']
            else:
                finished_finding_steps = True
                lines = step['remaining']

        return {
            'steps': steps,
            'remaining': lines,
            'raw_input': original_lines,
        }
