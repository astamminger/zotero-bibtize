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
    
