"""
Test for command line interface
"""

import shutil
import pathlib
from zotero_bibtize.cli import zotero_bibtize


def test_exception_on_missing_bib_file(tempcwd, click_runner):
    result = click_runner.invoke(zotero_bibtize, [])
    assert "No bibtex file found" in str(result.exception)
    assert result.exit_code != 0


def test_exception_on_multiple_bib_files(tempcwd, zotero_testfile, 
                                         wanted_testfile, click_runner):
    import shutil
    import pathlib
    # setup working directory
    shutil.copy(str(zotero_testfile), str(pathlib.Path('1.bib')))
    shutil.copy(str(zotero_testfile), str(pathlib.Path('2.bib')))
    # try to run the CLI without arguments which should fail on multiple
    # bib files present
    result = click_runner.invoke(zotero_bibtize, [])
    assert result.exit_code != 0
    assert "Multiple bibtex files found" in str(result.exception)


def test_call_without_outfile(tempcwd, zotero_testfile, wanted_testfile, 
                              click_runner):
    import shutil
    import pathlib
    # setup working directory
    shutil.copy(str(zotero_testfile), str(pathlib.Path('.')))
    # run conversion and check for success
    result = click_runner.invoke(zotero_bibtize, [])
    assert result.exit_code == 0
    # check that the backup file was created and that contents match with
    # original contents
    backup_file = tempcwd / '.{}.orig'.format(zotero_testfile.name)
    processed_file = tempcwd / zotero_testfile.name
    assert backup_file.exists()
    content_orig = open(str(zotero_testfile), 'r').read()
    content_backup = open(str(backup_file), 'r').read()
    assert content_orig == content_backup
    # finally compare processed result match wanted results
    content_processed = open(str(processed_file), 'r').read()
    content_wanted = open(str(wanted_testfile), 'r').read()
    print(content_processed)
    print(content_wanted)
#    assert content_processed == content_wanted


def test_call_with_outfile(tempcwd, zotero_testfile, wanted_testfile, 
                           click_runner):
    import shutil
    import pathlib
    # setup working directory
    shutil.copy(str(zotero_testfile), str(pathlib.Path('.')))
    # run conversion and check for success
    infile = zotero_testfile.absolute()
    outfile = tempcwd / 'processed.bib'
    result = click_runner.invoke(zotero_bibtize, [str(infile), str(outfile)])
    assert result.exit_code == 0
    content_processed = open(str(outfile), 'r').read()
    content_wanted = open(str(wanted_testfile), 'r').read()
    assert content_processed == content_wanted


def test_call_with_key_format(tempcwd, zotero_testfile, click_runner):
    import shutil
    import pathlib
    # setup working directory
    shutil.copy(str(zotero_testfile), str(pathlib.Path('.')))
    # run conversion and check for success
    infile = zotero_testfile.absolute()
    outfile = tempcwd / 'processed.bib'
    key_format = "[author:capitalize][journal:upper:abbreviate][year]"
    args = [str(infile), str(outfile), "--key-format", key_format]
    result = click_runner.invoke(zotero_bibtize, args)
    assert result.exit_code == 0
    content_processed = open(str(outfile), 'r').read()
    assert "ChenSSI2014" in content_processed
