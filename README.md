# Autodoc generation

- [Google style](https://google.github.io/styleguide/pyguide.html#381-docstrings) definitions

## Pdoc3

```bash
poetry add pdoc3
```

```bash
pdoc --html tests
start html\tests\index.html
```

See `html_helpers.py` to get _numpy_ and _google_ style parsing based on regexp.

## Mkdocs

```bash
poetry add mkdocs mkdocs-material mkdocstrings
mkdocs new .
```

```bash
mkdocs serve
```

!!! Supports only _Google_ style.

Ref. [Documenting a Python package with mkdocs-material](https://chrieke.medium.com/documenting-a-python-package-with-code-reference-via-mkdocs-material-b4a45197f95b).

## Sphinx

```bash
poetry add sphinx
```

```bash
mkdir sphinx
cd sphinx
sphinx-quickstart
> Separate source and build directories (y/n) [n]: y
> Project name: Sphinx Demo
> Author name(s): gs
> Project release []: 0.0.1
...

conf.py:

```python
import os
import sys
sys.path.insert(0, os.path.abspath("../../tests"))

extensions = [
    "sphinx.ext.napoleon",
]
```

```bash
sphinx-apidoc -f -o source/ ../tests
```

source/index.rst:

```rst
Welcome to sphinx demo's documentation!
=======================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
```

```bash
./make.bat html
start build/html/index.html
```

Ref. [Using Sphinx for Python Documentation](https://shunsvineyard.info/2019/09/19/use-sphinx-for-python-documentation/).

## Markdown for Sphinx

Ref. [Markdown](https://www.sphinx-doc.org/en/master/usage/markdown.html).
