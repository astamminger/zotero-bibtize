import pytest

@pytest.fixture
def empty_bibentry():
    from zotero_bibtize.zotero_bibtize import BibEntry
    class BibEntryEmpty(BibEntry):
        def __init__(self):
            pass
    yield BibEntryEmpty()


@pytest.fixture
def empty_bibtexfile():
    from zotero_bibtize.zotero_bibtize import BibTexFile
    class BibTexFileEmpty(BibTexFile):
        def __init__(self):
            pass
    yield BibTexFileEmpty()


@pytest.fixture
def click_runner():
    from click.testing import CliRunner
    yield CliRunner()


@pytest.fixture
def tempfolder():
    from tempfile import TemporaryDirectory
    import pathlib
    tempfolder = TemporaryDirectory()
    yield pathlib.Path(tempfolder.name)


@pytest.fixture
def tempcwd(tempfolder):
    import os
    import pathlib
    initial_cwd = os.getcwd()
    # change current working directory to the temporary folder
    os.chdir(str(tempfolder))
    yield tempfolder
    # change back to the original cwd after test has finished
    os.chdir(initial_cwd)


@pytest.fixture
def zotero_testfile():
    import pathlib
    root = pathlib.Path(__file__).parent
    yield root / 'cli' / 'test_data' / 'original_entry.bib'


@pytest.fixture
def wanted_testfile():
    import pathlib
    root = pathlib.Path(__file__).parent
    yield root / 'cli' / 'test_data' / 'wanted_entry.bib'
