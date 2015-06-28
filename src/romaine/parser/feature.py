from romaine.parser.exceptions import FeatureTrailingDataError

from copy import copy


class FeatureParser(object):
    """
        Gherkin feature parser for Romaine core.
    """
    def __init__(self, multiline_parser, section_parser):
        """
            Initialise feature parser.

            Keyword arguments:
            multiline_parser - An instance of a multiline parser.
            section_parser - An instance of a section parser.
        """
        self.multiline = multiline_parser
        self.section = section_parser

    def get_feature(self, lines):
        """
            Takes a set of lines and attempts to retrieve a feature from them.

            Keyword arguments:
            lines - list of lines to consume.

            Returns:
            Dict containing:
                feature - Dict containing:
                    header - List of lines in header (if any).
                    tags - List of tags (if any).
                    background - Background dict, if applicable.
                    leading_space_and_comments - List of leading space and
                                                 comments.
                    elements - List of scenarios and scenario outlines.
                    trailing_space_and_comments - List of trailing space and
                                                  comments.
                remaining - lines remaining after steps are consumed
                raw_input - The input data for this function
        """
        lines = copy(lines)
        original_lines = copy(lines)

        leading_space_and_comments = self.multiline.get_comments_with_space(
            lines,
        )
        lines = leading_space_and_comments['remaining']
        leading_space_and_comments = leading_space_and_comments[
            'comments_and_space']

        tags = self.multiline.get_tags(lines)
        lines = tags['remaining']
        tags = tags['tags']

        header = self.section.get_header(lines)
        lines = header['remaining']
        header = header['header']

        background = self.section.get_background(lines)
        lines = background['remaining']
        background = background['background']

        scenarios_and_outlines = self.section.get_elements(lines)
        lines = scenarios_and_outlines['remaining']
        scenarios_and_outlines = scenarios_and_outlines['elements']

        trailing_space_and_comments = self.multiline.get_comments_with_space(
            lines,
        )
        lines = trailing_space_and_comments['remaining']
        trailing_space_and_comments = trailing_space_and_comments[
            'comments_and_space']

        if len(lines) > 0:
            raise FeatureTrailingDataError(
                '{number} lines remaining: {lines}'.format(
                    number=len(lines),
                    lines=lines,
                )
            )

        return {
            'feature': {
                'header': header,
                'tags': tags,
                'background': background,
                'leading_space_and_comments': leading_space_and_comments,
                'elements': scenarios_and_outlines,
                'trailing_space_and_comments': trailing_space_and_comments,
            },
            'remaining': lines,
            'raw_input': original_lines,
        }
