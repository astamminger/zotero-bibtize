"""
Test BibTexFile class and methods
"""

import pytest

def test_num_to_char_mapping(empty_bibtexfile):
    import string
    single_chars = [c for c in string.ascii_lowercase]
    multi_chars = [c1+c2 for c1 in single_chars for c2 in single_chars]
    char_testlist = enumerate(single_chars + multi_chars)
    for (index, wanted_char) in char_testlist:
        assert empty_bibtexfile.num_to_char(index) == wanted_char
        

def test_strip_down_entries(empty_bibtexfile):
    # test for regular content string of length 20
    num_repetition = 5
    test_entry = "@  {    {} {     }  }"
    test_entry = num_repetition * test_entry
    wanted_indices = [(21*i, (21*i)+21) for i in range(num_repetition)]
    indices = empty_bibtexfile.strip_down_entries(test_entry)
    assert indices == wanted_indices
    # test proper error message is raised for unmatched braces
    test_entry = "@entrytype{ {  }"
    with pytest.raises(Exception) as exception:
        _ = empty_bibtexfile.strip_down_entries(test_entry)
    assert "Unbalanced braces error" in str(exception.value)


def test_resolve_unambigous_keys(empty_bibtexfile):
    # setup a fake class for bibtex entries holding a key value
    class FakeEntry(object):
        def __init__(self, keyvalue):
            self.key = keyvalue
    # create bibtexfile class with single and multiple keys
    empty_bibtexfile.entries = {
        0: FakeEntry('key_single'),
        1: FakeEntry('key_multi'),
        2: FakeEntry('key_multi'),
        3: FakeEntry('key_multi'),
    }
    # setup the corresponding key map
    empty_bibtexfile.key_map = {
        'key_single': [0],
        'key_multi': [1, 2, 3],
    }
    # assert that multiple keys get appended with a - z
    empty_bibtexfile.resolve_unambiguous_keys()
    assert empty_bibtexfile.entries[0].key == 'key_single'
    assert empty_bibtexfile.entries[1].key == 'key_multia'
    assert empty_bibtexfile.entries[2].key == 'key_multib'
    assert empty_bibtexfile.entries[3].key == 'key_multic'
