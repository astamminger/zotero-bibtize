# -*- coding: utf-8 -*-


import re
import collections

from zotero_bibtize.bibkey_formatter import KeyFormatter


class BibEntry(object):
    def __init__(self, bibtex_entry_string, key_format=None, omit_fields=None):
        # check for fields not required
        self.fields_to_omit = []
        if omit_fields is not None:
            self.fields_to_omit = omit_fields.split(',')
        self._raw = bibtex_entry_string
        entry_type, entry_key, entry_fields = self.entry_fields(self._raw)
        # set internal variables
        self.type = entry_type
        if key_format is not None:
            key_formatter = KeyFormatter(entry_fields, entry_type=entry_type)
            self.key = key_formatter.generate_key(key_format)
        else:
            self.key = entry_key
        self.fields = entry_fields
        
    def entry_fields(self, bibtex_entry_string):
        """Disassemble the bibtex entry contents."""
        # revert zotero escaping
        etype, ekey, econtent = self.bibtex_entry_contents(bibtex_entry_string)
        # disassemble the field entries (use ordered dict to assure output
        # order matches the input order for python versions < 3.6, this is not
        # of practical importance for generated bib-files but allows for 
        # easier tests based on file comparison)
        fields = collections.OrderedDict()
        for field in econtent:
            key, content = self.field_label_and_contents(field)
            # skip if field was set to be omitted
            if key in self.fields_to_omit: continue 
            fields[key] = content
        return etype, ekey, fields

    def field_label_and_contents(self, field):
        """Extract the field label and the corresponding content."""
        field, count = re.subn(r'^(\s*)|(\s*)$', '', field)
        # needs a separate expression for matching months which are
        # not exported with surrounding braces...
        regex = r'^([\s\S]*?)\s+\=\s+(?:\{([\s\S]*)\}|([\s\S]*)),*?$'
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
        entry_type, entry_content = entry_match.group(1, 2)
        # check if the unescaped bibtex entry is valid
        if not self._is_balanced(entry_content):
            raise Exception("Found braces unbalanced after unescaping of "
                            "BibTeX entry. The offending entry was\n\n"
                            "{}".format(raw_entry_string))
        entry_content = []
        tmp_entry = ''
        for part in re.split(r",", entry_match.group(2)):
            tmp_entry += re.sub(r'\n', '', part)
            # since _is_balanced also returns True for strings containing
            # no braces at this also works for the initial bibentry key
            if self._is_balanced(tmp_entry):
                entry_content.append(re.sub(r'\n', '', tmp_entry))
                tmp_entry = ''
            else:  # re-introduce comma if unbalanced
                tmp_entry += ','
        # remove possible emtpy entry at the end of the array
        if not entry_content[-1]:
            entry_content = entry_content[:-1]
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
        # use set(words) to prevent double replacements
        for word in set(words):
            entry = entry.replace(word, word.lstrip("{").rstrip("}"))
        return entry

    def _is_balanced(self, string):
        """
        Check if opening and closing curly braces are balanced in string.

        :param str string: string to be checked for balanced braces
        """
        n_open = len(re.findall(r"\{", string))
        n_close = len(re.findall(r"\}", string))
        return n_open == n_close

    def __str__(self):
        # return bibtex entry as string
        content = ['@{}{{{}'.format(self.type, self.key)]
        for (field_key, field_content) in self.fields.items():
            content.append('    {} = {{{}}}'.format(field_key, field_content))
        return ",\n".join(content) + '\n}\n'


class BibTexFile(object):
    """Bibtext file contents"""
    def __init__(self, bibtex_file, key_format=None, omit_fields=None):
        self.bibtex_file = bibtex_file
        self.entries = []
        self.key_map = collections.defaultdict(list)
        for (index, entry) in enumerate(self.parse_bibtex_entries()):
            bibentry = BibEntry(entry, key_format=key_format, 
                                omit_fields=omit_fields)
            self.entries.append(bibentry)
            self.key_map[bibentry.key].append(index)
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
                    try:
                        next_index, next_char = next(content_iterator)
                    except StopIteration:
                        raise Exception("Unbalanced braces error during the "
                                        "parsing of entry {}".format(content))
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
