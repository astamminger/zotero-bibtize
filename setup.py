# -*- coding: utf-8 -*-


import os

from setuptools import setup, find_packages


with open('README.md', 'r') as readme:
    long_description = readme.read()


setup(
    name="zotero-bibtize",
    version="0.0.1",
    author="Andreas Stamminger",
    author_email="stammingera@gmail.com",
    description="Transform Zotero BibTex files to LaTeX friendly representation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="Zotero Latex Bibtex",
    url="https://github.com/astamminger/zotero-bibtize",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3',
    install_requires=[
        "pathlib",
        "click",
    ],
    entry_points={
        'console_scripts': ['zotero-bibtize=zotero_bibtize.cli:zotero_bibtize'],
    },
)
