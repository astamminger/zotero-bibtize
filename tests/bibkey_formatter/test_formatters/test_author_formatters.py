"""
Test suite for BibKey formatting sequences.

Tests the generation of key contents based on the author entry
"""

from zotero_bibtize.bibkey_formatter import KeyFormatter

#
# Test lower author formatting
#
def test_no_author_lower():
    key_formatter = KeyFormatter({})
    key_format = '[author:lower]'
    assert key_formatter.generate_key(key_format) == 'noname'


def test_single_author_lower():
    authors = 'Surname, Firstname'
    key_formatter = KeyFormatter({'author': authors})
    key_format = '[author:lower]'
    assert key_formatter.generate_key(key_format) == 'surname'


def test_prefixed_author_lower():
    authors = 'Prefix Surname, Firstname'
    key_formatter = KeyFormatter({'author': authors})
    key_format = '[author:lower]'
    assert key_formatter.generate_key(key_format) == 'prefixsurname'


def test_multi_author_lower():
    authors = 'Surname, Firstname and Prefix Surname, Firstname'
    key_formatter = KeyFormatter({'author': authors})
    # default only first author
    key_format = '[author:lower]'
    assert key_formatter.generate_key(key_format) == 'surname'
    # use only one author (i.e. the first author)
    key_format = '[author:1:lower]'
    assert key_formatter.generate_key(key_format) == 'surname'
    # use two authors from the list
    key_format = '[author:2:lower]'
    assert key_formatter.generate_key(key_format) == 'surnameprefixsurname'
    # use maximal three authors
    key_format = '[author:3:lower]'
    assert key_formatter.generate_key(key_format) == 'surnameprefixsurname'


#
# Test upper author formatting
#
def test_no_author_upper():
    key_formatter = KeyFormatter({})
    key_format = '[author:upper]'
    assert key_formatter.generate_key(key_format) == 'NONAME'


def test_single_author_upper():
    authors = 'Surname, Firstname'
    key_formatter = KeyFormatter({'author': authors})
    key_format = '[author:upper]'
    assert key_formatter.generate_key(key_format) == 'SURNAME'


def test_prefixed_author_upper():
    authors = 'Prefix Surname, Firstname'
    key_formatter = KeyFormatter({'author': authors})
    key_format = '[author:upper]'
    assert key_formatter.generate_key(key_format) == 'PREFIXSURNAME'


def test_multi_author_upper():
    authors = 'Surname, Firstname and Prefix Surname, Firstname'
    key_formatter = KeyFormatter({'author': authors})
    # default only first author
    key_format = '[author:upper]'
    assert key_formatter.generate_key(key_format) == 'SURNAME'
    # use only one author (i.e. the first author)
    key_format = '[author:1:upper]'
    assert key_formatter.generate_key(key_format) == 'SURNAME'
    # use two authors from the list
    key_format = '[author:2:upper]'
    assert key_formatter.generate_key(key_format) == 'SURNAMEPREFIXSURNAME'
    # use maximal three authors
    key_format = '[author:3:upper]'
    assert key_formatter.generate_key(key_format) == 'SURNAMEPREFIXSURNAME'


#
# Test capitalized author formatting
#
def test_no_author_capitalize():
    key_formatter = KeyFormatter({})
    key_format = '[author:capitalize]'
    assert key_formatter.generate_key(key_format) == 'NoName'


def test_single_author_capitalize():
    authors = 'Surname, Firstname'
    key_formatter = KeyFormatter({'author': authors})
    key_format = '[author:capitalize]'
    assert key_formatter.generate_key(key_format) == 'Surname'


def test_prefixed_author_upper():
    authors = 'Prefix Surname, Firstname'
    key_formatter = KeyFormatter({'author': authors})
    key_format = '[author:capitalize]'
    assert key_formatter.generate_key(key_format) == 'PrefixSurname'


def test_multi_author_upper():
    authors = 'Surname, Firstname and Prefix Surname, Firstname'
    key_formatter = KeyFormatter({'author': authors})
    # default only first author
    key_format = '[author:capitalize]'
    assert key_formatter.generate_key(key_format) == 'Surname'
    # use only one author (i.e. the first author)
    key_format = '[author:1:upper]'
    key_format = '[author:1:capitalize]'
    assert key_formatter.generate_key(key_format) == 'Surname'
    # use two authors from the list
    key_format = '[author:2:capitalize]'
    assert key_formatter.generate_key(key_format) == 'SurnamePrefixSurname'
    # use maximal three authors
    key_format = '[author:3:capitalize]'
    assert key_formatter.generate_key(key_format) == 'SurnamePrefixSurname'


#
# Test abbreviated author formatting
#
def test_no_author_abbreviate():
    key_formatter = KeyFormatter({})
    key_format = '[author:abbreviate]'
    assert key_formatter.generate_key(key_format) == 'NN'
    key_formatter = KeyFormatter({})
    key_format = '[author:abbr]'
    assert key_formatter.generate_key(key_format) == 'NN'


def test_single_author_abbreviate():
    authors = 'Surname, Firstname'
    key_formatter = KeyFormatter({'author': authors})
    key_format = '[author:abbreviate]'
    assert key_formatter.generate_key(key_format) == 'S'
    key_format = '[author:abbr]'
    assert key_formatter.generate_key(key_format) == 'S'


def test_prefixed_author_abbreviate():
    authors = 'Prefix Surname, Firstname'
    key_formatter = KeyFormatter({'author': authors})
    key_format = '[author:abbreviate]'
    assert key_formatter.generate_key(key_format) == 'PS'
    key_format = '[author:abbr]'
    assert key_formatter.generate_key(key_format) == 'PS'


def test_multi_author_abbreviate():
    authors = 'Surname, Firstname and Prefix Surname, Firstname'
    key_formatter = KeyFormatter({'author': authors})
    # default only first author
    key_format = '[author:abbreviate]'
    assert key_formatter.generate_key(key_format) == 'S'
    key_format = '[author:abbr]'
    assert key_formatter.generate_key(key_format) == 'S'
    # use only one author (i.e. the first author)
    key_format = '[author:1:abbreviate]'
    assert key_formatter.generate_key(key_format) == 'S'
    key_format = '[author:1:abbr]'
    assert key_formatter.generate_key(key_format) == 'S'
    # use two authors from the list
    key_format = '[author:2:abbreviate]'
    assert key_formatter.generate_key(key_format) == 'SPS'
    key_format = '[author:2:abbr]'
    assert key_formatter.generate_key(key_format) == 'SPS'
    # use maximal three authors
    key_format = '[author:3:abbreviate]'
    assert key_formatter.generate_key(key_format) == 'SPS'
    key_format = '[author:3:abbr]'
    assert key_formatter.generate_key(key_format) == 'SPS'


def test_missing_author():
    """Test editor is used if author is missing"""
    key_format = '[author]'
    # check that editor is used if author not present
    editors = 'Surname, Firstname and Prefix Surname, Firstname'
    authors = '' 
    key_formatter = KeyFormatter({'author': authors, 'editor': editors})
    assert key_formatter.generate_key(key_format) == 'Surname'
    # check authors take precedence over editors
    editors = 'Editor, Firstname and Prefix Author, Firstname'
    authors = 'Author, Firstname and Prefix Author, Firstname'
    key_formatter = KeyFormatter({'author': authors, 'editor': editors})
    assert key_formatter.generate_key(key_format) == 'Author'
    # check No Name author is used if none is present
    editors = ''
    authors = '' 
    key_formatter = KeyFormatter({'author': authors, 'editor': editors})
    assert key_formatter.generate_key(key_format) == 'NoName'
