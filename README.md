# Readme

## Sphinx

- `poetry add Sphinx`
- `mkdir docs`
- `cd docs`
- `sphinx-quickstart`
     - `autodoc`
     -  - ...
- `poetry run make.bat html`
- `cd ..`
- `poetry run sphinx-apidoc -o docs/_modules src`


- `start docs/_build/html/index.html`
- see: [Using Sphinx for Python Documentation](https://shunsvineyard.info/2019/09/19/use-sphinx-for-python-documentation/)

## Mkdocs

- `poetry add mkdocs`
- `poetry add mkdocs-material`
- `poetry add mkdocstrings`
- `poetry run mkdocs new .`

mkdocs.yml

```yml

```

- see: [Documenting a Python package with mkdocs-material](https://chrieke.medium.com/documenting-a-python-package-with-code-reference-via-mkdocs-material-b4a45197f95b)
