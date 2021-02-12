import pprint

import pytest
from numpydoc.docscrape import FunctionDoc, Parameter, NumpyDocString


@pytest.fixture
def pp():
    return pprint.PrettyPrinter(indent=2)


# https://numpydoc.readthedocs.io/en/latest/format.html#sections


def sample_function(a: int, b: str):
    r"""
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


def test_numpydoc_function():
    doc = FunctionDoc(func=sample_function)
    assert doc["Parameters"] == [
        Parameter(name="a", type="int, default: 5", desc=["Does something cool"]),
        Parameter(name="b", type="str", desc=["Wow"]),
    ]
    assert doc["See Also"] == [([("blabla", None)], [])]
    assert doc["Notes"] == ["alias: blabla", "adesso tu"]


def test_numpydoc_string():
    doc = NumpyDocString(sample_function.__doc__)
    assert doc["Parameters"] == [
        Parameter(name="a", type="int, default: 5", desc=["Does something cool"]),
        Parameter(name="b", type="str", desc=["Wow"]),
    ]
    assert doc["See Also"] == [([("blabla", None)], [])]
    assert doc["Notes"] == ["alias: blabla", "adesso tu"]
