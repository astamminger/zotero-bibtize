"""
Test suite for BibKey formatting sequences.

Tests the generation of key contents based on the journal entry
"""

from zotero_bibtize.bibkey_formatter import KeyFormatter

#
# Test lower journal formatting
#
def test_no_journal_lower():
    key_formatter = KeyFormatter({})
    key_format = '[journal:lower]'
    assert key_formatter.generate_key(key_format) == 'noname'


#
# Test upper journal formatting
#
def test_no_journal_upper():
    key_formatter = KeyFormatter({})
    key_format = '[journal:upper]'
    assert key_formatter.generate_key(key_format) == 'NONAME'


#
# Test capitalized journal formatting
#
def test_no_journal_capitalize():
    key_formatter = KeyFormatter({})
    key_format = '[journal:capitalize]'
    assert key_formatter.generate_key(key_format) == 'NoName'


#
# Test abbreviated journal formatting
#
def test_no_journal_abbreviate():
    key_formatter = KeyFormatter({})
    key_format = '[journal:abbreviate]'
    assert key_formatter.generate_key(key_format) == 'NN'
    key_formatter = KeyFormatter({})
    key_format = '[journal:abbr]'
    assert key_formatter.generate_key(key_format) == 'NN'
