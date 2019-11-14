# -*- coding: utf-8 -*-


import os

from setuptools import setup, find_packages


setup(
    name="zotero-bibtize",
    version="0.0.1",
    author="Andreas Stamminger",
    author_email="stammingera@gmail.com",
    description="Transform Zotero BibTex files to LaTeX friendly representation.",
    long_description="",
    keywords="",
    url="",
    packages=find_packages(),
    classifiers=[
        ''
    ],
    install_requires=[
        "pathlib",
        "click",
    ],
    entry_points={
        'console_scripts': ['zotero-bibtize=cli:zotero_bibtize'],
    },
)
