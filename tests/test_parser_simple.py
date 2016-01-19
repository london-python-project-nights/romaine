from tests import common
import unittest


class TestSimpleParser(unittest.TestCase):
    """
        Test single line gherkin parser functionality of romaine's core.
    """
    def setUp(self):
        """
            Prepare the environment for testing.
        """
        pass

    def tearDown(self):
        """
            Revert changes made during testing.
        """
        pass

    def test_white_matches_empty_line(self):
        """
            Check the is_white call matches an empty line.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call is_white on an empty string
        result = parser.simple.is_white('')

        # Then the result is True
        self.assertTrue(result)

    def test_white_matches_spaces(self):
        """
            Check the is_white call matches spaces.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call is_white on a string containing only spaces
        result = parser.simple.is_white('         ')

        # Then the result is True
        self.assertTrue(result)

    def test_white_matches_tabs(self):
        """
            Check the is_white call matches tabs.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call is_white on a string containing only tabs
        result = parser.simple.is_white('\t\t\t\t')

        # Then the result is True
        self.assertTrue(result)

    def test_white_matches_spaces_and_tabs(self):
        """
            Check the is_white call matches mixed tabs and spaces.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call is_white on a string with tabs and spaces
        result = parser.simple.is_white(' \t\t  \t  \t\t\t')

        # Then the result is True
        self.assertTrue(result)

    def test_white_does_not_match_non_space(self):
        """
            Check the is_white call does not match non-whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call is_white on a string with non-whitespace
        result = parser.simple.is_white('  sdg     ')

        # Then the result is False
        self.assertFalse(result)

    def test_fail_to_get_tag_line(self):
        """
            Confirm that we get no tag when a line doesn't contain one.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tag on a string with no @
        result = parser.simple.get_tag('  there is no tag')

        # Then the result is None
        self.assertIsNone(result)

    def test_get_simple_tag(self):
        """
            Check that we get the expected tag for a simple tag.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tag on '  @simple_tag'
        result = parser.simple.get_tag('  @simple_tag')

        # Then the result is simple_tag
        self.assertEqual(result, 'simple_tag')

    def test_fail_get_tag_with_at_sign(self):
        """
            Confirm that we get no tag when tag contains @.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tag on '  @tag@ten'
        result = parser.simple.get_tag('  @tag@ten')

        # Then the result is None
        self.assertIsNone(result)

    def test_fail_get_tag_tab(self):
        """
            Confirm that we get no tag when a tag contains tabs.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tag on '  @test\ttag'
        result = parser.simple.get_tag('  @test\ttag')

        # Then the result is None
        self.assertIsNone(result)

    def test_fail_get_tag_with_space(self):
        """
            Confirm that we get no tag when a tag contains space.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tag on '  @my tag is here'
        result = parser.simple.get_tag('  @my tag is here')

        # Then the result is None
        self.assertIsNone(result)

    def test_fail_get_empty_tag(self):
        """
            Confirm that we get no tag when it is empty.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call get_tag on '  @'
        result = parser.simple.get_tag('  @')

        # Then the result is None
        self.assertIsNone(result)

    def test_pythonish_multiline_delimiter(self):
        """
            Confirm that \"\"\" are recognised as multiline string delimiter.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call is_multiline_delimiter on '"""'
        result = parser.simple.is_multiline_delimiter('"""')

        # Then the result is True
        self.assertTrue(result)

    def test_pythonish_multiline_delimiter_with_space(self):
        """
            Confirm that \"\"\" are recognised as multiline string delimiter.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call is_multiline_delimiter on '  """\t'
        result = parser.simple.is_multiline_delimiter('  """\t')

        # Then the result is True
        self.assertTrue(result)

    def test_pythonish_multiline_opening_delimiter_with_trailing_text(self):
        """
            Confirm that trailing characters permitted on opening delimiters.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call is_multiline_delimiter on '"""ttt'
        result = parser.simple.is_multiline_delimiter('"""ttt')

        # Then the result is True
        self.assertTrue(result)

    def test_pythonish_multiline_closing_delimiter_with_trailing_text(self):
        """
            Confirm trailing characters not permitted on closing delimiters.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call is_multiline_delimiter on '"""ttt' for closing delimiter
        result = parser.simple.is_multiline_delimiter('"""ttt', closing=True)

        # Then the result is False
        self.assertFalse(result)

    def test_not_pythonish_multiline_delimiter(self):
        """
            Confirm that \" \"\" not recognised as multiline string delimiter.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call is_multiline_delimiter on '  """'
        result = parser.simple.is_multiline_delimiter('" ""')

        # Then the result is False
        self.assertFalse(result)

    def test_pythonish_multiline_delimiter_wrong_quotes(self):
        """
            Confirm that ''' not recognised as multiline string delimiter.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call is_multiline_delimiter on "'''"
        result = parser.simple.is_multiline_delimiter("'''")

        # Then the result is False
        self.assertFalse(result)

    def test_pythonish_multiline_delimiter_leading_noise(self):
        """
            Confirm multiline delimiters not recognised with leading noise.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I call is_multiline_delimiter on ' notspaces """'
        result = parser.simple.is_multiline_delimiter(' notspaces """')

        # Then the result is False
        self.assertFalse(result)

    def test_comment_line(self):
        """
            Confirm comment line is detected with no leading whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I test whether '# something' is a comment
        result = parser.simple.is_comment('# something')

        # Then the result is True
        self.assertTrue(result)

    def test_comment_leading_whitespace(self):
        """
            Confirm commentline is detected with leading whitespace.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I test whether '   \t#3f;3w[g3-[g;3s--5e5' is a comment
        result = parser.simple.is_comment('   \t#3f;3w[g3-[g;3s--5e5')

        # Then the result is True
        self.assertTrue(result)

    def test_not_comment(self):
        """
            Confirm comments are not detected with preceding characters.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I test whether 'mmm# something' is a comment
        result = parser.simple.is_comment('mmm# something')

        # Then the result is False
        self.assertFalse(result)

    def test_get_one_cell(self):
        """
            Confirm that we can retrieve a single cell.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get cells from '|test|'
        result = parser.simple.get_cells('|test|')

        # Then the result is ['test']
        self.assertEqual(result, ['test'])

    def test_get_one_cell_indented(self):
        """
            Confirm that we can retrieve a single indented cell.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get cells from '\t  \t|test|'
        result = parser.simple.get_cells('\t  \t|test|')

        # Then the result is ['test']
        self.assertEqual(result, ['test'])

    def test_get_no_cell(self):
        """
            Confirm that we don't get cells when none exist.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get cells from 'test'
        result = parser.simple.get_cells('test')

        # Then the result is None
        self.assertIsNone(result)

    def test_get_one_cell_non_space_indented(self):
        """
            Confirm that we cannot retrieve a cell indented with non spaces.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get cells from '  ttt |test|'
        result = parser.simple.get_cells('  ttt |test|')

        # Then the result is None
        self.assertIsNone(result)

    def test_get_multiple_cells(self):
        """
            Confirm that we can retrieve multiple cells.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get cells from '|test|123| |2.1|[123]|{123:4}|'
        result = parser.simple.get_cells(
            '|test|123| |2.1|[123]|{123:4}|'
        )

        # Then the result is ['test','123',' ','2.1','[123]','{123:4}']
        self.assertEqual(
            result,
            [
                'test',
                '123',
                ' ',
                '2.1',
                '[123]',
                '{123:4}',
            ]
        )

    def test_fail_to_get_broken_cells(self):
        """
            Confirm that we cannot retrieve where an empty cell exists.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get cells from '|test||'
        result = parser.simple.get_cells('|test||')

        # Then the result is None
        self.assertIsNone(result)

    def test_fail_to_get_half_cell(self):
        """
            Confirm that we cannot retrieve a half cell.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get cells from '|test'
        result = parser.simple.get_cells('|test')

        # Then the result is None
        self.assertIsNone(result)

    def test_fail_to_get_cells_with_trailing_noise(self):
        """
            Confirm that we cannot retrieve cells if there is trailing data.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get cells from '|test|test2'
        result = parser.simple.get_cells('|test|test2')

        # Then the result is None
        self.assertIsNone(result)

    def test_fail_to_get_just_opening_cell(self):
        """
            Confirm that we cannot retrieve just the opening of a cell.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get cells from '  |'
        result = parser.simple.get_cells('  |')

        # Then the result is None
        self.assertIsNone(result)

    def test_get_given_step(self):
        """
            Confirm that we can retrieve a 'Given' step.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get step from 'Given some spam'
        result = parser.simple.get_step('Given some spam')

        # Then the result is a step of type Given with text of 'some spam'
        self.assertEqual(
            result,
            {
                'type': 'Given',
                'text': 'some spam',
            }
        )

    def test_get_when_step(self):
        """
            Confirm that we can retrieve a 'When' step.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get step from 'When some spam'
        result = parser.simple.get_step('When some spam')

        # Then the result is a step of type When with text of 'some spam'
        self.assertEqual(
            result,
            {
                'type': 'When',
                'text': 'some spam',
            }
        )

    def test_get_then_step(self):
        """
            Confirm that we can retrieve a 'Then' step.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get step from 'Then some spam'
        result = parser.simple.get_step('Then some spam')

        # Then the result is a step of type Then with text of 'some spam'
        self.assertEqual(
            result,
            {
                'type': 'Then',
                'text': 'some spam',
            }
        )

    def test_get_and_step(self):
        """
            Confirm that we can retrieve a 'And' step.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get step from 'And some spam'
        result = parser.simple.get_step('And some spam')

        # Then the result is a step of type And with text of 'some spam'
        self.assertEqual(
            result,
            {
                'type': 'And',
                'text': 'some spam',
            }
        )

    def test_get_but_step(self):
        """
            Confirm that we can retrieve a 'But' step.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get step from 'But some spam'
        result = parser.simple.get_step('But some spam')

        # Then the result is a step of type But with text of 'some spam'
        self.assertEqual(
            result,
            {
                'type': 'But',
                'text': 'some spam',
            }
        )

    def test_get_indented_step(self):
        """
            Confirm that we can retrieve a step when indented by spaces/tabs.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get step from ' \t \t But some spam'
        result = parser.simple.get_step(' \t \t But some spam')

        # Then the result is a step of type But with text of 'some spam'
        self.assertEqual(
            result,
            {
                'type': 'But',
                'text': 'some spam',
            }
        )

    def test_fail_get_incorrectly_named_step(self):
        """
            Confirm that we do not retrieve a step when not named correctly.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get step from ' \t \t Butter some spam'
        result = parser.simple.get_step(' \t \t Butter some spam')

        # Then the result is None
        self.assertIsNone(result)

    def test_get_step_with_hash(self):
        """
            Confirm that we can retrieve a step with a hash in it.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get step from ' \t \t But some spam has #'
        result = parser.simple.get_step(' \t \t But some spam has #')

        # Then the result is a step of type But with text of 'some spam has #'
        self.assertEqual(
            result,
            {
                'type': 'But',
                'text': 'some spam has #',
            }
        )

    def test_get_step_with_trailing_spaces(self):
        """
            Confirm that we can retrieve a step with trailing spaces.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get step from ' \t \t But spam   \t  '
        result = parser.simple.get_step(' \t \t But spam   \t  ')

        # Then the result is a step of type But with text of 'spam   \t  '
        self.assertEqual(
            result,
            {
                'type': 'But',
                'text': 'spam   \t  ',
            }
        )

    def test_fail_get_step_with_tab(self):
        """
            Confirm that we fail to retrieve a step name with a following tab.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I try to get step from 'But\t spam is here'
        result = parser.simple.get_step('But\t spam is here')

        # Then the result is None.
        self.assertIsNone(result)

    def test_get_examples_section_start_with_whitespace(self):
        """
            Confirm that we can detect the noisy start of an examples section.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I see if an example section is started with
        # '  \t Examples:  \t '
        result = parser.simple.get_section_start('  \t Examples:  \t ')

        # Then the type is examples with a description of '  \t '
        self.assertEqual(
            result,
            {
                'type': 'examples',
                'description': '  \t ',
            },
        )

    def test_get_examples_section_start_without_whitespace(self):
        """
            Confirm that we can detect the start of an examples section.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I see if an example section is started with 'Examples:'
        result = parser.simple.get_section_start('Examples:')

        # Then the type is examples with a description of ''
        self.assertEqual(
            result,
            {
                'type': 'examples',
                'description': '',
            },
        )

    def test_get_section_start_trailing_character_failure(self):
        """
            Confirm that section is started with a description.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I see if an example section is started with
        # '  \t Scenario: f3fvs2'
        result = parser.simple.get_section_start('  \t Scenario: f3fvs2')

        # Then the type is scenario with a description of ' f3fvs2'
        self.assertEqual(
            result,
            {
                'type': 'scenario',
                'description': ' f3fvs2',
            },
        )

    def test_is_examples_section_start_trailing_character_failure(self):
        """
            Confirm that section is not started with leading characters.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I see if a section is started with 'ffab12 Examples:'
        result = parser.simple.get_section_start('ffab12 Examples:')

        # Then the there is no type or description
        self.assertEqual(
            result,
            {
                'type': None,
                'description': None,
            },
        )

    def test_get_scenario_section_start_with_whitespace(self):
        """
            Confirm that we can detect the noisy start of a scenario section.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I see if an example section is started with
        # '  \t Scenario:  \t '
        result = parser.simple.get_section_start('  \t Scenario:  \t ')

        # Then the type is scenario with a description of '  \t '
        self.assertEqual(
            result,
            {
                'type': 'scenario',
                'description': '  \t ',
            },
        )

    def test_get_scenario_section_start_without_whitespace(self):
        """
            Confirm that we can detect the start of a scenario section.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I see if an example section is started with 'Scenario:'
        result = parser.simple.get_section_start('Scenario:')

        # Then the type is scenario with a description of ''
        self.assertEqual(
            result,
            {
                'type': 'scenario',
                'description': '',
            },
        )

    def test_get_scenario_outline_section_start_with_whitespace(self):
        """
            Confirm that we can detect the noisy start of a scenario outline.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I see if an example section is started with
        # '  \t Scenario Outline:  \t '
        result = parser.simple.get_section_start('  \t Scenario Outline:  \t ')

        # Then the type is scenario outline with a description of '  \t '
        self.assertEqual(
            result,
            {
                'type': 'scenario outline',
                'description': '  \t ',
            },
        )

    def test_get_scenario_outline_section_start_without_whitespace(self):
        """
            Confirm that we can detect the start of a scenario outline.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I see if an example section is started with 'Scenario Outline:'
        result = parser.simple.get_section_start('Scenario Outline:')

        # Then the type is scenario outline with a description of ''
        self.assertEqual(
            result,
            {
                'type': 'scenario outline',
                'description': '',
            },
        )

    def test_get_background_section_start_with_whitespace(self):
        """
            Confirm that we can detect the noisy start of a background section.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I see if an example section is started with
        # '  \t Background:  \t '
        result = parser.simple.get_section_start('  \t Background:  \t ')

        # Then the type is background with a description of '  \t '
        self.assertEqual(
            result,
            {
                'type': 'background',
                'description': '  \t ',
            },
        )

    def test_get_background_section_start_without_whitespace(self):
        """
            Confirm that we can detect the start of a background section.
        """
        # Given I have Romaine core's parser
        parser = common.get_romaine_parser()

        # When I see if an example section is started with 'Background:'
        result = parser.simple.get_section_start('Background:')

        # Then the type is background with a description of ''
        self.assertEqual(
            result,
            {
                'type': 'background',
                'description': '',
            },
        )
