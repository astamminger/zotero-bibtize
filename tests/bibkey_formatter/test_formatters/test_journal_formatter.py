"""
Test suite for BibKey formatting sequences.

Tests the generation of key contents based on the title
"""

from zotero_bibtize.bibkey_formatter import KeyFormatter

#
# Test lower journal formatting
#
def test_no_journal_lower():
    key_formatter = KeyFormatter({})
    key_format = '[journal:lower]'
    assert key_formatter.generate_key(key_format) == 'nojournal'
    journal = "Chemistry of Materials"
    key_formatter = KeyFormatter({"journal": journal})
    key_format = '[journal:lower]'
    assert key_formatter.generate_key(key_format) == 'chemistrymaterials'


#
# Test upper journal formatting
#
def test_no_journal_upper():
    key_formatter = KeyFormatter({})
    key_format = '[journal:upper]'
    assert key_formatter.generate_key(key_format) == 'NOJOURNAL'
    journal = "Chemistry of Materials"
    key_formatter = KeyFormatter({"journal": journal})
    key_format = '[journal:upper]'
    assert key_formatter.generate_key(key_format) == 'CHEMISTRYMATERIALS'


#
# Test capitalized journal formatting
#
def test_no_journal_capitalize():
    key_formatter = KeyFormatter({})
    key_format = '[journal:capitalize]'
    assert key_formatter.generate_key(key_format) == 'NoJournal'
    journal = "Chemistry of Materials"
    key_formatter = KeyFormatter({"journal": journal})
    key_format = '[journal:capitalize]'
    assert key_formatter.generate_key(key_format) == 'ChemistryMaterials'


#
# Test abbreviated journal formatting
#
def test_no_journal_abbreviate():
    key_formatter = KeyFormatter({})
    key_format = '[journal:abbreviate]'
    assert key_formatter.generate_key(key_format) == 'NJ'
    key_formatter = KeyFormatter({})
    key_format = '[journal:abbr]'
    assert key_formatter.generate_key(key_format) == 'NJ'
    journal = "Chemistry of Materials"
    key_formatter = KeyFormatter({"journal": journal})
    key_format = '[journal:abbreviate]'
    assert key_formatter.generate_key(key_format) == 'CM'


def test_omit_no_journal_if_book():
    """
    Check that journal is not replaced with 'No Journal' in books and
    book sections
    """
    # check for book sections
    key_formatter = KeyFormatter({}, entry_type='incollection')
    key_format = '[journal:abbreviate]'
    assert key_formatter.generate_key(key_format) == ''
    # check for book
    key_formatter = KeyFormatter({}, entry_type='book')
    key_format = '[journal:abbreviate]'
    assert key_formatter.generate_key(key_format) == ''
    # check for all other cases
    key_formatter = KeyFormatter({}, entry_type=None)
    key_format = '[journal:abbreviate]'
    assert key_formatter.generate_key(key_format) == 'NJ'
    
