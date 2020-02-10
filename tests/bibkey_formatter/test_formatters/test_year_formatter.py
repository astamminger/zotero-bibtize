"""
Test suite for BibKey formatting sequences.

Tests the generation of key contents based on the publication year entry
"""

from zotero_bibtize.bibkey_formatter import KeyFormatter

def test_year_long():
    """Test empty year is replace with 0000."""
    format_args = '[year:long]'
    # empty year should evaluate to 0000
    key_formatter = KeyFormatter({})
    expected_year = '0000'
    formatted_year = key_formatter.generate_key(format_args)
    assert formatted_year == expected_year
    # test real year
    key_formatter = KeyFormatter({'year': '2008'})
    expected_year = '2008'
    formatted_year = key_formatter.generate_key(format_args)
    assert formatted_year == expected_year


def test_year_short():
    """Test empty year is replace with 0000."""
    key_formatter = KeyFormatter({})
    format_args = '[year:short]'
    # empty year should evaluate to 0000
    formatted_year = key_formatter.generate_key(format_args)
    expected_year = '00'
    assert formatted_year == expected_year
    # test real year
    key_formatter = KeyFormatter({'year': '2008'})
    expected_year = '08'
    formatted_year = key_formatter.generate_key(format_args)
    assert formatted_year == expected_year
