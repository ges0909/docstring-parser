from sphinxcontrib.napoleon import Config, NumpyDocstring

# Napoleon is a Sphinx extension that enables Sphinx to parse both NumPy and Google style docstrings.
# sections: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/

config = Config(napoleon_use_param=True, napoleon_use_rtype=True)

sample = r"""
    Something something

    Parameters
    ----------
    a : int, default: 5
         Does something cool
    b : str
         Wow

    See Also
    --------
    blabla

    Notes
    -----
    alias: blabla
    adesso tu
    """


def test_sphinx_napaleon():
    doc = NumpyDocstring(docstring=sample, config=config)
    print(doc.lines())
