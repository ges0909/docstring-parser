from sphinxcontrib.napoleon import Config, NumpyDocstring

# Napoleon is a Sphinx extension that enables Sphinx to parse both NumPy and Google style docstrings.
# sections: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/

config = Config(napoleon_use_param=True, napoleon_use_rtype=True)


def test_sphinx_napaleon(benchmark):
    """
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
    # doc = NumpyDocstring(docstring=sample, config=config)
    doc = benchmark(NumpyDocstring, docstring=test_sphinx_napaleon.__doc__, config=config)
    print("\n".join(doc.lines()))
