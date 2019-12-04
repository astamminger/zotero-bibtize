# -*- coding: utf-8 -*-


import re

# key format
# [field1:formatter]


class KeyGen(object):
    def __init__(self, bibtex_entry):
        self.bibtex_entry = bibtex_entry
        self.field_format_map = {
            'author': self.format_author_key,
            'year': self.format_year_key,
        }

    def generate_key_entry(self, key_format):
        """Generate a bibtex key according to the defined format."""
        format_list = self.unpack_format_entries(key_format)
        bibkey = key_format
        for ((field, format_actions), raw) in format_list:
            formatted_key = self.field_format_map[field](*format_actions)
            formatter = "[{}]".format(raw)
            bibkey = bibkey.replace(formatter, formatted_key)
            print(bibkey)

    def unpack_format_entries(self, key_format):
        """Extract the format entries from the total key_format string."""
        format_regex = r"\[(.*?)\]"
        format_entries = re.findall(format_regex, key_format)
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

    def format_author_key(self, *format_args):
        """Generate formatted author key entry."""
        authors = self.bibtex_entry.fields['author']
        authors = self.remove_latex_content(authors)
        # determine how many authors to use
        if re.match(r"\d+", format_args[0]):
            N_entry = int(format_args[0])
            format_args = format_args[1:]
        else:  # default number of authors is one
            N_entry = 1
        author_list = [lastname.strip() for author in authors.split('and') 
                                        for lastname in author.split(',')[:1]] 
        # do not use more than N_entry author names for the entry
        author_list = author_list[:N_entry]
        for format_arg in format_args:
            author_list = self.apply_format_to_content(author_list, format_arg)    
        return "".join(author_list)

    def format_year_key(self, *format_args):
        """Generate formatted year key entry."""
        year = self.bibtex_entry.fields['year']
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


#def format_year_key(bibtex_entry, N, *format_args):
#    pass
#
#
#def format_journal_key(bibtex_entry, N, *format_args):
#    pass
#
#
#def format_title_key(bibtex_entry, N, *format_args):
#    pass
#
# [authorsN:upper:abbreviate]
# upper -> uppercase
# abbreviate -> only first letter


if __name__ == "__main__":
    key_format = "[authors:upper:abbreviate][year][journal:capitalize:abbreviate]"
    extract_format_entries(key_format)
