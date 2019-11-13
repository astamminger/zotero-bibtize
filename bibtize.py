#!/usr/bin/env python

import re
import pathlib

class BibEntry(object):
    def __init__(self, bibtex_entry_string):
        self._raw = bibtex_entry_string
        entry_type, entry_key, entry_fields = self.entry_fields(self._raw)
        # set internal variables
        self.type = entry_type
        self.key = entry_key
        self.fields = entry_fields
        
    def entry_fields(self, bibtex_entry_string):
        """Disassemble the bibtex entry contents."""
        # revert zotero escaping
        etype, ekey, econtent = self.bibtex_entry_contents(bibtex_entry_string)
        # disassemble the field entries
        fields = {}
        for field in econtent:
            key, content = self.field_label_and_contents(field)
            fields[key] = content
        return etype, ekey, fields

    def field_label_and_contents(self, field):
        """Extract the field label and the corresponding content."""
        field, count = re.subn(r'^(\s*)|(\s*)$', '', field)
        # needs a separate expression for matching months which are
        # not exported with surrounding braces...
        regex = r'^([\s\S]*)\s+\=\s+(?:\{([\s\S]*)\}|([a-z]{3})),*?$'
        fmatch = re.match(regex, field)
        field_key = fmatch.group(1)
        field_content = fmatch.group(2) or fmatch.group(3)
        return field_key, field_content

    def bibtex_entry_contents(self, raw_entry_string):
        """Unescape the entry string and get the contained contents."""
        # revert zotero escpaing and remove trailing / leading whitespaces
        unescaped = self.unescape_bibtex_entry_string(raw_entry_string)
        unescaped = re.sub(r'^(\s*)|(\s*)$', '', unescaped)
        entry_match = re.match(r'^\@([\s\S]*?)\{([\s\S]*?)\}$', unescaped)
        entry_type = entry_match.group(1)
        entry_content =  re.split(',\n', entry_match.group(2))
        # return type, original zotero key and the actual content list 
        return (entry_type, entry_content[0], entry_content[1:])
            

    def unescape_bibtex_entry_string(self, entry):
        """Remove zotero escapes and additional braces."""
        entry = self.remove_zotero_escaping(entry)
        entry = self.remove_special_char_escaping(entry)
        entry = self.remove_curly_from_capitalized(entry)
        return entry

    def remove_zotero_escaping(self, entry):
        # first we remove the escape sequences defined by Zotero
        zotero_escaping_map = {
	        r"|": r"\{\\textbar\}",
	        r"<": r"\{\\textless\}",
	        r">": r"\{\\textgreater\}",
	        r"~": r"\{\\textasciitilde\}",
	        r"^": r"\{\\textasciicircum\}",
	        r"\\": r"\{\\textbackslash\}",
	        r"{" : r"\\{\\vphantom{\\}}",
	        r"}" : r"\\vphantom{\\{}\\}"
        }
        for (replacement, escape_sequence) in zotero_escaping_map.items():
            entry, subs = re.subn(escape_sequence, replacement, entry)
        return entry
    
    def remove_special_char_escaping(self, entry):
        zotero_special_chars = {
            r"#": r"\\#",
            r"%": r"\\%",
            r"&": r"\\&",
            r"_": r"\\_",
            r"{": r"\\{",
            r"}": r"\\}",
        }
        for (replacement, escape_sequence) in zotero_special_chars.items():
            entry, subs = re.subn(escape_sequence, replacement, entry)
        return entry

    def remove_curly_from_capitalized(self, entry):
        """Remove the implicit curly braces added to capitalized words."""
        # next remove the implicit curly braces around capitalized words
        #regex = r"\{[A-Z][^\s]*?\}"
        regex = r"\{[A-Z][\w]*?\}"
        words = re.findall(regex, entry)
        for word in words:
            entry = entry.replace(word, word.lstrip("{").rstrip("}"))
        return entry


class BibTex(object):
    """Bibtext contents"""
    def __init__(self, bibtex_file=None):
        if bibtex_file is None:
            cwd = pathlib.Path('.').absolute()
            bibtex_files = cwd.glob('*.bib')
            if len(bibtex_files) > 1:
                raise Exception("Found multiple bibtex files in the current "
                                "location '{}'. Pleas specify an explicit "
                                "file to use!".format(bibtex_files))
            elif len(bibtex_fils) == 0:
                raise Exception("No bibtex file found at the current location "
                                "'{}'".format(str(cwd)))
            bibtex_file = bibtex_files[0]
        else:
            bibtex_file = pathlib.Path(bibtex_file)
            if bibtex_file.exists() is False:
                raise Exception("The passed bibtex file '{}' does not exist"
                                .format(str(bibtex_file)))
        self.bibtex_file = bibtex_file
        self.entries = self.parse_bibtex_entries()

    def parse_bibtex_entries(self):
        """Parse entries from file."""
        bibtex_content_str = self.load_bibtex_contents()
        entry_locations = self.strip_down_entries(bibtex_content_str)
        entries = []
        for (entry_start, entry_stop) in entry_locations:
            entry_str = bibtex_content_str[entry_start:entry_stop]
            entries.append(entry_str)
        return entries

    def load_bibtex_contents(self):
        """Load the file contents into a string."""
        with open(self.bibtex_file, 'r') as bibfile:
            contents = bibfile.read()
        return contents
    
    def strip_down_entries(self, content):
        """Identify single entries in the bibtex output file."""
        content_iterator = enumerate(content)
        bibtex_entries = []
        for (index, char) in content_iterator:
            if char == '@':
                start_index = index
            if char == '{':
                stack = 1
                while stack != 0:
                    next_index, next_char = next(content_iterator)
                    if next_char == '}':
                        stack -= 1
                    elif next_char == '{':
                        stack += 1
                bibtex_entries.append((start_index, next_index+1))
        return bibtex_entries
    
    def remove_zotero_escaping_from_entry(self, entry):
        """Remove zotero escapes and additional braces."""
        zotero_escaping_map = {
	        r"|": r"\{\\textbar\}",
	        r"<": r"\{\\textless\}",
	        r">": r"\{\\textgreater\}",
	        r"~": r"\{\\textasciitilde\}",
	        r"^": r"\{\\textasciicircum\}",
	        r"\\": r"\{\\textbackslash\}",
#	        // See http://tex.stackexchange.com/questions/230750/open-brace-in-bibtex-fields/230754
	        r"{" : r"\\{\\vphantom{\\}}",
	        r"}" : r"\\vphantom{\\{}\\}"
        }
        # finish off the defined replacements
        for (replacement, escape_sequence) in zotero_escaping_map.items():
            entry, subs = re.subn(escape_sequence, replacement, entry)
        # next remove the implicit curly braces around capitalized words
        regex = r"\{[A-Z][^\s]*?\}"
        words = re.findall(regex, entry)
        for word in words:
        #    print(word)
            entry = entry.replace(word, word.lstrip("{").rstrip("}"))
#        # un-escape everything that is neither a number nor a char
#        regex = r"\\[^A-Za-z0-9]"
#        escaped_chars = re.findall(regex, entry)
#        for escaped_char in escaped_chars:
#            unescaped_char = escaped_char.lstrip(r"\\")
#            entry = entry.replace(escaped_char, unescaped_char)
#        print(entry)
        return entry

if __name__ == "__main__":
    btex = BibTex('./Diss.bib')
    for entry in btex.entries:
        e = BibEntry(entry)
#        print(e.key)
        print("{}: {}".format(e.type, e.key))
