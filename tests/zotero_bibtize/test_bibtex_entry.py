import pytest

# Custom escapes added by Zotero 
zotero_escapes = [
    (r"{\textbar}", "|"),
    (r"{\textless}", "<"),
    (r"{\textgreater}", ">"),
    (r"{\textasciitilde}", "~"),
    (r"{\textasciicircum}", "^"),
    (r"{\textbackslash}", "\\"),
    (r"\{\vphantom{\}}", "{"),
    (r"\vphantom{\{}\}", "}"),
]
@pytest.mark.parametrize(('escaped_input', 'wanted_output'), zotero_escapes)
def test_remove_zotero_custom_escapes(empty_bibentry, escaped_input, 
                                      wanted_output):
    """Test Zotero escapes are properly removed."""
    unescaped = empty_bibentry.remove_zotero_escaping(escaped_input)
    assert unescaped == wanted_output


# Special chars escaped by Zotero
zotero_escapes = [
    (r"\#", "#"),
    (r"\%", "%"),
    (r"\&", "&"),
    (r"\$", "$"),
    (r"\_", "_"),
    (r"\{", "{"),
    (r"\}", "}"),
]
@pytest.mark.parametrize(('escaped_input', 'wanted_output'), zotero_escapes)
def test_remove_zotero_special_chars_escapes(empty_bibentry, escaped_input, 
                                             wanted_output):
    """Test Zotero escapes are properly removed."""
    unescaped = empty_bibentry.remove_special_char_escaping(escaped_input)
    assert unescaped == wanted_output


def test_remove_curly_braces_from_capitalized(empty_bibentry):
    # test at beginning of string
    test_str = "{Capitalized} with curly braces"
    wanted = "Capitalized with curly braces"
    processed = empty_bibentry.remove_curly_from_capitalized(test_str)
    assert processed == wanted
    # test in the middle of strings
    test_str = "capitalized {With} {Curly} braces" 
    wanted = "capitalized With Curly braces" 
    processed = empty_bibentry.remove_curly_from_capitalized(test_str)
    assert processed == wanted
    # test at end of string
    test_str = "capitalized with curly {Braces}" 
    wanted = "capitalized with curly Braces" 
    processed = empty_bibentry.remove_curly_from_capitalized(test_str)
    assert processed == wanted
    # leave non-capitalized words alone
    test_str = "capitalized {with} {curly} braces" 
    wanted = "capitalized {with} {curly} braces" 
    processed = empty_bibentry.remove_curly_from_capitalized(test_str)
    assert processed == wanted

#
# Entry types known by BibTex according to 
# http://texdoc.net/texmf-dist/doc/bibtex/base/btxdoc.pdf
#
bibtex_entry_types = [
    "article",
    "book",
    "booklet",
    "conference",
    "incollection",
    "inproceedings",
    "manual",
    "mastersthesis",
    "misc",
    "phdthesis",
    "proceedings",
    "techreport",
    "unpublished",
]
@pytest.mark.parametrize(('bibtex_entry_type'), bibtex_entry_types)
def test_entry_type_is_recognized(bibtex_entry_type):
    from zotero_bibtize.zotero_bibtize import BibEntry
    #entry_string = (r"@{:}{{key,{{field = {{}}}}"
    #                .format(bibtex_entry_type))
    entry_string = r"@{:}{{key,{{}}".format(bibtex_entry_type)
    bibentry = BibEntry(entry_string)
    # check parsed type matches wanted type
    assert bibentry.type == bibtex_entry_type
    # check that no fields were passed, i.e. the fields dictionary is
    # expected to be empty
    assert bibentry.fields == {}


#
# Field names known by BibTex according to 
# http://texdoc.net/texmf-dist/doc/bibtex/base/btxdoc.pdf
#
def test_bibtex_fields_are_recognized():
    from zotero_bibtize.zotero_bibtize import BibEntry
    valid_fields = [
        "address",
        "annote",
        "author",
        "booktitle",
        "chapter",
        "crossref",
        "edition",
        "editor",
        "collection",
        "howpublished",
        "institution",
        "journal",
        "key",
        "month",
        "work",
        "abbreviation",
        "note",
        "number",
        "organization",
        "pages",
        "publisher",
        "school",
        "series",
        "title",
        "type",
        "volume",
        "year",
    ]
    fields_string = ",\n".join(["{} = {{}}".format(f) for f in valid_fields])
    entry_string = "@bibtextype{{bibentry_key,\n{}}}".format(fields_string)
    bibentry = BibEntry(entry_string)
    # check parsed type and key match the set ones
    assert bibentry.type == "bibtextype"
    assert bibentry.key == "bibentry_key"
    # check that all field names were parsed but no field values were set
    # (i.e. since no match will be found the entries should have been set 
    # to none!)
    for field in valid_fields:
        assert field in bibentry.fields.keys()
        assert bibentry.fields[field] is None


def test_output_string_assembly():
    from zotero_bibtize.zotero_bibtize import BibEntry
    input_entry = (
        "@bibtextype{bibkey,",
        "    field1 = {contents of field 1},",
        "    field2 = {contents of field 2},",
        "    field3 = {¢ontents of field 3}",
        "}",
        "",  # account for additional newline to separate entries
    )
    input_entry = "\n".join(input_entry)
    bibentry = BibEntry(input_entry)
    output_entry = str(bibentry)
    assert input_entry == output_entry


def test_field_label_and_contents(empty_bibentry):
    # test for regular field of type fielname = {content}
    wanted_field_name = "fieldname"
    wanted_field_content = "Contents of the field"
    test_string = "{} = {{{}}}".format(wanted_field_name, wanted_field_content)
    field, content = empty_bibentry.field_label_and_contents(test_string)
    assert field == wanted_field_name
    assert content == wanted_field_content
    # test for field of type fieldname = content
    wanted_field_name = "fieldname"
    wanted_field_content = "Contents without braces"
    test_string = "{} = {}".format(wanted_field_name, wanted_field_content)
    field, content = empty_bibentry.field_label_and_contents(test_string)
    assert field == wanted_field_name
    assert content == wanted_field_content
    #
    # Test for issue (bug when content contains equality signs)
    # https://github.com/astamminger/zotero-bibtize/issues/6
    #
    wanted_field_name = "fieldname"
    wanted_field_content = "Contents with A = B equal C=D signs"
    test_string = "{} = {{{}}}".format(wanted_field_name, wanted_field_content)
    field, content = empty_bibentry.field_label_and_contents(test_string)
    assert field == wanted_field_name
    assert content == wanted_field_content


def test_ignore_custom_fields():
    from zotero_bibtize.zotero_bibtize import BibEntry
    input_entry = (
        "@bibtextype{bibkey,",
        "    field1 = {contents of field 1},",
        "    field2 = {contents of field 2},",
        "    field3 = {contents of field 3}",
        "}",
        "",  # account for additional newline to separate entries
    )
    input_entry = "\n".join(input_entry)
    # check for one field
    ignore_fields = "field1"
    bibentry = BibEntry(input_entry, omit_fields=ignore_fields)
    assert "field1" not in bibentry.fields.keys()
    assert "field2" in bibentry.fields.keys()
    assert "field3" in bibentry.fields.keys()
    # check for multiple fields
    ignore_fields = "field1,field3"  # string defined by CLI
    bibentry = BibEntry(input_entry, omit_fields=ignore_fields)
    assert "field1" not in bibentry.fields.keys()
    assert "field1" not in bibentry.fields.keys()
    assert "field2" in bibentry.fields.keys()

def test_fields_containing_equal_signs():
    from zotero_bibtize.zotero_bibtize import BibEntry
    input_entry = (
        "@bibtextype{bibkey,",
        "    field1 = {has no equal sign},",
        "    field2 = {contains an = sign},",
        "    field3 = {has no equal sign},",
        "}",
        "",  # account for additional newline to separate entries
    )
    input_entry = "\n".join(input_entry)
    bibentry = BibEntry(input_entry)
    assert bibentry.fields['field1'] == "has no equal sign"
    assert bibentry.fields['field2'] == "contains an = sign"
    assert bibentry.fields['field3'] == "has no equal sign"

def test_multiple_replacement_of_capitalized():
    """
    Test multiple latex commands are not replaced multiple times.

    In case of latex comands with capitalized contents constructs like
    \\ce{{Li4P2S6}} can occur. Along with a second entry of the form
    {Li4P2S6} in the entry the command would be replaced twice leading
    to outputs of the form \\ceLi4P2S6
    """
    from zotero_bibtize.zotero_bibtize import BibEntry
    # setup entry with fields containing multiple recurring capitalized
    # words (i.e. embraced by curly braces)
    input_entry = (
        "@bibtextype{bibkey,",
        "    field1 = {Has \\ce{{Command}}},",
        "    field2 = {Has same \\ce{{Command}}}",
        "}",
        "",
    )
    input_entry = "\n".join(input_entry)
    bibentry = BibEntry(input_entry)
    assert bibentry.fields['field1'] == "Has \\ce{Command}"
    assert bibentry.fields['field2'] == "Has same \\ce{Command}"
