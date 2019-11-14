# zotero-bibtize
Refurbish exported Zotero-BibTex bibliographies into a more LaTeX friendly representation

Before zotero-bibtize (as exported from Zotero):
```
	@article{LangCM2015,
		title = {Lithium {Ion} {Conduction} in {\textbackslash}ce\{{LiTi}2({PO}4)3\} and {Related} {Compounds} {Based} on the \{{NASICON}\} {Structure}: {A} {First}-{Principles} {Study}},
		volume = {27},
		issn = {0897-4756, 1520-5002},
		shorttitle = {Lithium {Ion} {Conduction} in {\textbackslash}ce\{{LiTi}2({PO}4)3\} and {Related} {Compounds} {Based} on the {NASICON} {Structure}},
		url = {http://pubs.acs.org/doi/10.1021/acs.chemmater.5b01582},
		doi = {10.1021/acs.chemmater.5b01582},
		language = {en},
		number = {14},
		urldate = {2019-02-11},
		journal = {Chem. Mater.},
		author = {Lang, Britta and Ziebarth, Benedikt and Els{\textbackslash}"\{a\}sser, Christian},
		month = jul,
		year = {2015},
		pages = {5040--5048}
	}
```

After zotero-bibtize:
```
	@article{LangCM2015,
	        title = {Lithium Ion Conduction in \ce{LiTi2(PO4)3} and Related Compounds Based on the NASICON Structure: A First-Principles Study},
	        volume = {27},
	        issn = {0897-4756, 1520-5002},
	        shorttitle = {Lithium Ion Conduction in \ce{LiTi2(PO4)3} and Related Compounds Based on the NASICON Structure},
	        url = {http://pubs.acs.org/doi/10.1021/acs.chemmater.5b01582},
	        doi = {10.1021/acs.chemmater.5b01582},
	        language = {en},
	        number = {14},
	        urldate = {2019-02-11},
	        journal = {Chem. Mater.},
	        author = {Lang, Britta and Ziebarth, Benedikt and Els\"{a}sser, Christian},
	        month = jul,
	        year = {2015},
	        pages = {5040--5048}
	}
```
