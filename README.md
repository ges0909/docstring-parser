# Readme

## Overview

|        | pdoc3 | Numpydoc | Sphinx | mkdocs |
| ------ | :---: | :------: | :----: | :----: |
| ReST   |   -   |    -     |        |   -    |
| numpy  |   +   |    +     |        |   -    |
| google |   +   |    -     |        |   +    |

## Self implemented

see: [Google style](https://google.github.io/styleguide/pyguide.html#381-docstrings) definitions

## Pdoc3

```bash
poetry add pdoc3
poetry run pdoc --html tests
start html\tests\index.html
```

See `html_helpers.py` to get _numpy_ and _google_ parsing.

## Sphinx

```bash
poetry add Sphinx
mkdir docs
cd docs
sphinx-quickstart
poetry run make.bat html
cd ..
poetry run sphinx-apidoc -o docs/_modules src
start docs/_build/html/index.html
```

see: [Using Sphinx for Python Documentation](https://shunsvineyard.info/2019/09/19/use-sphinx-for-python-documentation/)

## Mkdocs

```bash
poetry add mkdocs
poetry add mkdocs-material
poetry add mkdocstrings
poetry run mkdocs new .
poetry run mkdocs serve
```

!!! Supports only _Google_ style.

see: [Documenting a Python package with mkdocs-material](https://chrieke.medium.com/documenting-a-python-package-with-code-reference-via-mkdocs-material-b4a45197f95b)
