# -*- coding: utf-8 -*-


import click
import pathlib
import shutil

from zotero_bibtize import BibTexFile


@click.command()
@click.argument('input_file', type=click.Path(exists=True), default='.', 
                required=False)
@click.argument('output_file', type=click.Path(exists=False), default='.', 
                required=False)
def zotero_bibtize(input_file, output_file):
    """
    Transform Zotero BibTex files to LaTeX friendly representation.

    Reads in the bibtex contents of the `input_file` (if undefined the bibtex
    file in the current working directory will be used) and process its
    contents. Processed contents are then written back to the `output_file`
    (if undefined the input file will be overwritten!)
    """
    # check input path
    input_path = pathlib.Path(input_file).absolute()
    if input_path.is_dir():
        bib_files = list(input_path.glob('*.bib'))
        if len(bib_files) == 0:
            raise Exception("No bibtex file found at the given location.")
        elif len(bib_files) > 1:
            raise Exception("Multiple bibtex files found at the given "
                            "location, please select an explicit file.")
        bib_in = bib_files[0]
    else:  # input_path.is_file()
        if input_path.suffix != '.bib':
            raise Exception("Given file is not of type bibtex file.")
        bib_in = input_path
    # check output path
    output_path = pathlib.Path(output_file).absolute()
    bib_backup = bib_in.with_name('.' + bib_in.name).with_suffix('.bib.orig')
    if output_path.is_dir():
        shutil.copyfile(bib_in, bib_backup)
        bib_out = bib_in
    else:  # output_path.is_file()
        # check if the same file is specified and backup if yes
        if output_path == input_path:
            shutil.copyfile(bib_in, bib_backup)
        bib_out = output_path
    # read in and write processed contents back  
    bibliography = BibTexFile(str(bib_in))
    with open(bib_out, 'w') as bib_out_file:
        bib_out_file.write(''.join(map(str, bibliography.entries)))
