# -*- coding: utf-8 -*-


import re
import collections

from zotero_bibtize.bibkey_formatter import KeyFormatter


class BibEntry(object):
    def __init__(self, bibtex_entry_string, key_format=None):
        self._raw = bibtex_entry_string
        entry_type, entry_key, entry_fields = self.entry_fields(self._raw)
        # set internal variables
        self.type = entry_type
        if key_format is not None:
            self.key = KeyFormatter(entry_fields).generate_key(key_format)
        else:
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
        regex = r'^([\s\S]*)\s+\=\s+(?:\{([\s\S]*)\}|([\s\S]*)),*?$'
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
            r"#": r"\\\#",
            r"%": r"\\\%",
            r"&": r"\\\&",
            r"$": r"\\\$",
            r"_": r"\\\_",
            r"{": r"\\\{",
            r"}": r"\\\}",
        }
        for (replacement, escape_sequence) in zotero_special_chars.items():
            entry, subs = re.subn(escape_sequence, replacement, entry)
        return entry

    def remove_curly_from_capitalized(self, entry):
        """Remove the implicit curly braces added to capitalized words."""
        # next remove the implicit curly braces around capitalized words
        regex = r"\{[A-Z][\w]*?\}"
        words = re.findall(regex, entry)
        for word in words:
            entry = entry.replace(word, word.lstrip("{").rstrip("}"))
        return entry

    def __str__(self):
        # return bibtex entry as string
        content = ['@{}{{{}'.format(self.type, self.key)]
        for (field_key, field_content) in self.fields.items():
            content.append('    {} = {{{}}}'.format(field_key, field_content))
        return ",\n".join(content) + '\n}\n'


class BibTexFile(object):
    """Bibtext file contents"""
    def __init__(self, bibtex_file, key_format=None):
        self.bibtex_file = bibtex_file
        self.entries = []
        self.key_map = collections.defaultdict(list)
        for (index, entry) in enumerate(self.parse_bibtex_entries()):
            entry = BibEntry(entry, key_format=key_format)
            self.entries.append(entry)
            self.key_map[entry.key].append(index)
        self.resolve_unambiguous_keys()

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

    def num_to_char(self, number):
        """
        Map the given number on chars a-z.

        All numbers N for 0 <= N <= 25 will be mapped on the chars a-z
        and numbers N > 25 will be mapped on the chars aa-zz.

        :param int number: number transformed to char representation
        """
        offset = ord('a')
        minor = number % 26
        major = number // 26 - 1
        return chr(offset + major) * (major >= 0)  + chr(offset + minor)

    def resolve_unambiguous_keys(self):
        """Resolve ambiguous bibtex keys."""
        for (key, indices) in self.key_map.items():
            # do nothing if the key is unique already
            if len(indices) == 1: continue
            # otherwise append a-z / aa-zz to the key
            for (i, index) in enumerate(indices):
                self.entries[index].key = key + self.num_to_char(i)
