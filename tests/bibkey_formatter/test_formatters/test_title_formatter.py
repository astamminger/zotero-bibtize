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
    key_format = '[title:lower]'
    assert key_formatter.generate_key(key_format) == 'notitle'
    test_title = ("Segregation of sp-impurities at grain boundaries and "
                  "surfaces")
    key_formatter = KeyFormatter({'title': test_title})
    key_format = '[title:lower]'
    # by default max three words are used to generate the key and special char
    # like '-' and function words should be removed
    generated_key = key_formatter.generate_key(key_format)
    assert generated_key == "segregationspimpuritiesgrain"
    


#
# Test upper journal formatting
#
def test_no_journal_upper():
    key_formatter = KeyFormatter({})
    key_format = '[title:upper]'
    assert key_formatter.generate_key(key_format) == 'NOTITLE'
    test_title = ("Segregation of sp-impurities at grain boundaries and "
                  "surfaces")
    key_formatter = KeyFormatter({'title': test_title})
    key_format = '[title:upper]'
    # by default max three words are used to generate the key and special char
    # like '-' and function words should be removed
    generated_key = key_formatter.generate_key(key_format)
    assert generated_key == "SEGREGATIONSPIMPURITIESGRAIN"


#
# Test capitalized journal formatting
#
def test_no_journal_capitalize():
    key_formatter = KeyFormatter({})
    key_format = '[title:capitalize]'
    assert key_formatter.generate_key(key_format) == 'NoTitle'
    test_title = ("Segregation of sp-impurities at grain boundaries and "
                  "surfaces")
    key_formatter = KeyFormatter({'title': test_title})
    key_format = '[title:capitalize]'
    # by default max three words are used to generate the key and special char
    # like '-' and function words should be removed
    generated_key = key_formatter.generate_key(key_format)
    assert generated_key == "SegregationSpimpuritiesGrain"


#
# Test abbreviated journal formatting
#
def test_no_journal_abbreviate():
    key_formatter = KeyFormatter({})
    key_format = '[title:abbreviate]'
    assert key_formatter.generate_key(key_format) == 'NT'
    key_formatter = KeyFormatter({})
    key_format = '[title:abbr]'
    assert key_formatter.generate_key(key_format) == 'NT'
    test_title = ("Segregation of sp-impurities at grain boundaries and "
                  "surfaces")
    key_formatter = KeyFormatter({'title': test_title})
    key_format = '[title:abbreviate]'
    # by default max three words are used to generate the key and special char
    # like '-' and function words should be removed
    generated_key = key_formatter.generate_key(key_format)
    assert generated_key == "Ssg"


#
# Test number of words used from title
#
def test_number_of_title_words():
    test_title = ("Segregation of sp-impurities at grain boundaries and "
                  "surfaces")
    key_formatter = KeyFormatter({'title': test_title})
    # default use three words
    key_format = '[title:lower]'
    generated_key = key_formatter.generate_key(key_format)
    assert generated_key == "segregationspimpuritiesgrain"
    # test all words from title
    key_format = '[title:5:lower]'
    generated_key = key_formatter.generate_key(key_format)
    assert generated_key == "segregationspimpuritiesgrainboundariessurfaces"
    # test num words exceeding the total number of available words
    key_format = '[title:9:lower]'
    generated_key = key_formatter.generate_key(key_format)
    assert generated_key == "segregationspimpuritiesgrainboundariessurfaces"
    # test zero words is valid
    key_format = '[title:0:lower]'
    generated_key = key_formatter.generate_key(key_format)
    assert generated_key == ""
