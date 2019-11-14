# -*- coding: utf-8 -*-


import click
import pathlib

from zotero_bibtize import BibTex


@click.command()
@click.argument('path', type=click.Path(exists=True), default='.', 
                required=False)
def zotero_bibtize(path):
    """
    Transform Zotero BibTex files to LaTeX friendly representation.
    """
    path = pathlib.Path(path).absolute()
    if path.is_dir():
        bibtex_files = list(path.glob('*.bib'))
        if len(bibtex_files) == 0:
            raise Exception("No bibtex file found at the given location.")
        elif len(bibtex_files) > 1:
            raise Exception("Multiple bibtex files found at the given "
                            "location, please select an explicit file.")
        bibtex_file = bibtex_files[0]
    elif path.is_file():
        if path.suffix != '.bib':
            raise Exception("Given file is not of type bibtex file.")
        bibtex_file = path
    bibliography = BibTex(str(bibtex_file))
    print(bibliography.entries)
