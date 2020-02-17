"""
Test module for interal bibkey formatter functions
"""

import pytest

from zotero_bibtize.bibkey_formatter import KeyFormatter

def test_unpack_format_entries():
    """Test unpacking for format definitions."""
    key_formatter = KeyFormatter({})
    # test for a single field 
    format_entry = '[field1:option1:option2]'
    expected_content = [
        (('field1', ['option1', 'option2']), 'field1:option1:option2'),
    ] 
    unpacked_content = key_formatter.unpack_format_entries(format_entry)
    for (unpacked, expected) in zip(unpacked_content, expected_content):
        assert unpacked == expected
    # test for multiple fields 
    format_entry = '[field1:option1][field2:option1:option2][field3:option1]'
    expected_content = [
        (('field1', ['option1']), 'field1:option1'),
        (('field2', ['option1', 'option2']), 'field2:option1:option2'),
        (('field3', ['option1']), 'field3:option1'),
    ] 
    unpacked_content = key_formatter.unpack_format_entries(format_entry)
    for (unpacked, expected) in zip(unpacked_content, expected_content):
        assert unpacked == expected
    # test no options
    format_entry = '[field1]'
    expected_content = [
        (('field1', []), 'field1'),
    ] 
    unpacked_content = key_formatter.unpack_format_entries(format_entry)
    for (unpacked, expected) in zip(unpacked_content, expected_content):
        assert unpacked == expected
    # test emtpy format options raise
    format_entry = ''
    with pytest.raises(Exception) as exception:
        unpacked_content = key_formatter.unpack_format_entries(format_entry)
    assert "no valid format entries found" in str(exception.value)


def test_remove_math_environments():
    """Test for latex contents being properly removed from title strings."""
    key_formatter = KeyFormatter({})
    # check math environments are removed from string
    math_title = (r"This is a title containing $\mathrm{environments}$ with "
                   "$$\frac{latex}{math}$$ command definitions")
    title = key_formatter.remove_math_environments(math_title)
    # note that removing math environment will cause two consecutive empty
    # spaces when removed inside the string
    assert title == "This is a title containing  with  command definitions"


def test_remove_latex_commands():
    """Test removal of latex commands from title strings."""
    key_formatter = KeyFormatter({})
    # check latex commands \command{content} are replaced by the pure contents,
    # i.e. \command{content} --> {content}
    math_title = r"\latexcommand{applied to content}"
    title = key_formatter.remove_latex_commands(math_title)
    assert title == r"{applied to content}"
    math_title = r"\frac{multiple}{arguments}"
    title = key_formatter.remove_latex_commands(math_title)
    assert title == r"{multiple}{arguments}"


def test_remove_curly_braces():
    """Test removal of additional curly braces from title strings."""
    key_formatter = KeyFormatter({})
    # single word
    math_title = r"{Argument}"
    title = key_formatter.remove_curly_braces(math_title)
    assert title == r"Argument"
    # multiple words
    math_title = r"{applied to content}"
    title = key_formatter.remove_curly_braces(math_title)
    assert title == r"applied to content"
    # mixed title
    math_title = r"{Title} with {mixed contents}"
    title = key_formatter.remove_curly_braces(math_title)
    assert title == r"Title with mixed contents"


def test_function_words_removal():
    """Test function words are properly deleted from title strings"""
    key_formatter = KeyFormatter({})
    # a list of function words as defined by JabRef
    # (cf. https://docs.jabref.org/setup/bibtexkeypatterns)
    function_words_list =  [
        "a", "an", "the", "above", "about", "across", "against", "along", 
        "among", "around", "at", "before", "behind", "below", "beneath", 
        "beside", "between", "beyond", "by", "down", "during", "except", 
        "for", "from", "in", "inside", "into", "like", "near", "of", "off", 
        "on", "onto", "since", "to", "toward", "through", "under", "until",
        "up", "upon", "with", "within", "without", "and", "but", "for", 
        "nor", "or", "so", "yet"
    ]
    title_string = " ".join(function_words_list)
    title = key_formatter.remove_function_words(title_string)
    assert title == ""
    # check that the match is really case insensitive
    function_words_upper = [f.upper() for f in function_words_list]
    title_string = " ".join(function_words_list)
    title = key_formatter.remove_function_words(title_string)
    assert title == ""
    # test for a real title
    title_string = (r"A climbing image nudged elastic band method for "
                     "finding saddle points and minimum energy paths")
    title = key_formatter.remove_function_words(title_string)
    expected_string = (r"climbing image nudged elastic band method "
                        "finding saddle points minimum energy paths")
    assert title == expected_string


def test_function_words_removal_for_journals():
    """
    For Journals function keys should not match at the end of strings to
    preserve 'A' in journal names like Journal of Materials Chemistry A
    or Physical Review A, etc.
    """
    key_formatter = KeyFormatter({})
    journal_string = "Journal of Materials Chemistry A"
    # test behavior if is_journal is not set
    string_no_journal = key_formatter.remove_function_words(journal_string)
    assert string_no_journal == "Journal Materials Chemistry"
    # test behavior if is_journal is set
    string_is_journal = key_formatter.remove_function_words(journal_string,
                                                            is_journal=True)
    assert string_is_journal == "Journal Materials Chemistry A"
    # assert 'a' inside the journal name is removed
    journal_string = "Chemistry A European Journal"
    string_is_journal = key_formatter.remove_function_words(journal_string,
                                                            is_journal=True)
    assert string_is_journal == "Chemistry European Journal"
