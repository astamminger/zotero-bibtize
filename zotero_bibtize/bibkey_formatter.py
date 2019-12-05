# -*- coding: utf-8 -*-


import re


class KeyFormatter(object):
    def __init__(self, bibtex_fields):
        self.bibtex_fields = bibtex_fields
        self.field_format_map = {
            'author': self.format_author_key,
            'year': self.format_year_key,
            'journal': self.format_journal_key,
            'title': self.format_title_key,
        }

    def generate_key(self, key_format):
        """Generate a bibtex key according to the defined format."""
        format_list = self.unpack_format_entries(key_format)
        bibkey = key_format
        for ((field, format_actions), raw) in format_list:
            formatted_key = self.field_format_map[field](*format_actions)
            formatter = "[{}]".format(raw)
            bibkey = bibkey.replace(formatter, formatted_key)
        return bibkey

    def unpack_format_entries(self, key_format):
        """Extract the format entries from the total key_format string."""
        format_regex = r"\[(.*?)\]"
        format_entries = re.findall(format_regex, key_format)
        if not format_entries:
            raise Exception("no valid format entries found in defined key "
                            "format '{}'".format(key_format))
        format_list = []
        for format_entry in format_entries:
            entry_type, *format_actions = format_entry.split(':')
            format_list.append((entry_type, format_actions))
        return zip(format_list, format_entries)
        
    def apply_format_to_content(self, content, format_action):
        """ 
        Apply format actions to every word contained in content list
        
        :param list content: A list of words describing the content
        :param str format_action: String describing the format to apply
        """
        if format_action in ['upper']:
            return [c.upper() for c in content]
        elif format_action in ['lower']:
            return [c.lower() for c in content]
        elif format_action in ['capitalize']:
            return [c.capitalize() for c in content]
        elif format_action in ['abbreviate', 'abbr']:
            return [c[0] for c in content]
        else:
            raise Exception("Unknown format action: {}".format(format_action))
            
    def remove_latex_content(self, content_string):
        """Remove all latex contents from the given string."""
        content_string = self.remove_math_environments(content_string)
        content_string = self.remove_latex_commands(content_string)
        content_string = self.remove_curly_braces(content_string)
        return content_string

    def remove_latex_commands(self, content_string):
        """
        Remove latex commands from the given string.
    
        In this case only the latex command will be removed, i.e. a command
        of the form \command{content} will be replaced by {content}
        """
        latex_command_regex = r"(\\[^\{]+)\{"
        return re.sub(latex_command_regex, '', content_string).strip()

    def remove_math_environments(self, content_string):
        """
        Remove a latex math environment from the given string.

        This function will completely remove latex math environments from
        the string. It will only remove environments defined by either
        $ (inline) or $$. (will not remove environments initialized by
        \begin{equation},...)
        """
        latex_math_regex = r"\$+[\s\S]+?\$+"
        return re.sub(latex_math_regex, '', content_string).strip()

    def remove_curly_braces(self, content_string):
        """Remove curly braces from the given string."""
        curly_braces_regex = r"[\{\}]"
        return re.sub(curly_braces_regex, '', content_string).strip()

    def remove_function_words(self, content_string):
        """Remove all function words from the given string."""
        # a list of function words as defined by JabRef
        # (cf. https://docs.jabref.org/setup/bibtexkeypatterns)
        function_words_list =  [
            "a", "an", "the", "above", "about", "across", "against", "along", 
            "among", "around", "at", "before", "behind", "below", "beneath", 
            "beside", "between", "beyond", "by", "down", "during", "except", 
            "for", "from", "in", "inside", "into", "like", "near", "of", "off", 
            "on", "onto", "since", "to", "toward", "through", "under", "until",
            "up", "upon", "with", "within", "without", "and", "but", "for", 
            "nor", "or", "so", "yet"
        ]
        # join single words with regex 'or' operator
        function_words = "|".join(function_words_list)
        word_regex = r"(?:^|(?<=\s))({})(?:(?=\s)|$)".format(function_words)
        content_string = re.sub(word_regex, '', content_string).strip()
        # remove consecutive whitespaces
        content_string = re.sub(r"\s+", " ", content_string)
        return content_string

    def format_author_key(self, *format_args):
        """Generate formatted author key entry."""
        authors = self.bibtex_fields.get('author', 'None')
        authors = self.remove_latex_content(authors)
        N_entry = 1  # default number of authors to use for the entry
        if len(format_args) != 0:
            if re.match(r"\d+", format_args[0]):
                N_entry = int(format_args[0])
                format_args = format_args[1:]
        author_list = [lastname.strip() for author in authors.split('and') 
                                        for lastname in author.split(',')[:1]] 
        # do not use more than N_entry author names for the entry
        author_list = author_list[:N_entry]
        for format_arg in format_args:
            author_list = self.apply_format_to_content(author_list, format_arg)    
        return "".join(author_list)

    def format_year_key(self, *format_args):
        """Generate formatted year key entry."""
        year = self.bibtex_fields.get('year', '0000')
        # silently ignore additional format commands
        if len(format_args) == 0:
            format_args = "long"
        else:
            format_args = format_args[0]
        # check if arguments are valid
        if format_args not in ["long", "short"]:
            raise Exception("unknown format argument {} for year (allowed "
                            "arguments are 'short' or 'long')"
                            .format(format_args))
        if format_args == 'short':
            return year[2:]
        else:
            return year

    def format_journal_key(self, *format_args):
        """Generate formatted journal key entry."""
        journal = self.bibtex_fields.get('journal', 'None')
        if len(format_args) != 0:
            if re.match(r"\d+", format_args[0]):
                raise Exception("cannot define the number of words to use for "
                                "the journal key format")
        journal = self.remove_latex_content(journal)
        journal = re.sub(r"[^[A-Za-z0-9\s]", '', journal)
        journal = self.remove_function_words(journal)
        journal_list = journal.split(' ')
        for format_arg in format_args:
            journal_list = self.apply_format_to_content(journal_list, 
                                                        format_arg)    
        return "".join(journal_list)

    def format_title_key(self, *format_args):
        """Generate formatted title key entry."""
        title = self.bibtex_fields.get('title', 'None')
        title = self.remove_latex_content(title)
        N_entry = 3  # default number of words to use for the entry
        if len(format_args) != 0:
            if re.match(r"\d+", format_args[0]):
                N_entry = int(format_args[0])
                format_args = format_args[1:]
        title = re.sub(r"[^[A-Za-z0-9\s]", '', title)
        title = self.remove_function_words(title)
        # do not use more than N_entry title words for the entry
        title_list = title.split(' ')[:N_entry]
        for format_arg in format_args:
            title_list = self.apply_format_to_content(title_list, format_arg)    
        return "".join(title_list)
