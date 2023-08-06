Run pytest unit tests written as Jupyter notebooks:

* Collects all exceptions raised in each notebook
* Links to HTML notebook outputs in pytest output
* (Optionally) check notebook standard output per cell with methods `check_notebook_name(self, soup)` using [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

See tests/example.py.
