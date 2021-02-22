import pprint

import pytest
from numpydoc.docscrape import FunctionDoc, Parameter, NumpyDocString


@pytest.fixture
def pp():
    return pprint.PrettyPrinter(indent=2)


# https://numpydoc.readthedocs.io/en/latest/format.html#sections


@pytest.mark.skip
def test_numpydoc_function():
    r"""
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int, default: 5
        Description of arg1
    arg2 : str
        Description of arg2
    arg3 : str
        The [JMESpath](https://jmespath.org) query.

    Returns
    -------
    bool
        Description of return value

    Raises
    ------
    AttributeError
        The ``Raises`` section is a list of all exceptions
        that are relevant to the interface.
    ValueError
        If `arg2` is equal to `arg1`.

    Examples
    --------
    Examples should be written in doctest format, and should illustrate how
    to use the function.

    >>> a=1
    >>> b=2
    >>> func(a,b)
    True

    Notes
    -----
    blabla

    """
    doc = FunctionDoc(func=test_numpydoc_function.__doc__)
    assert doc["Parameters"] == [
        Parameter(name="a", type="int, default: 5", desc=["Does something cool"]),
        Parameter(name="b", type="str", desc=["Wow"]),
    ]
    assert doc["See Also"] == [([("blabla", None)], [])]
    assert doc["Notes"] == ["alias: blabla", "adesso tu"]


def test_numpydoc_string(benchmark):
    r"""
    Summary line.

    Extended description of function.

    Parameters
    ----------
    arg1 : int, default: 5
        Description of arg1
    arg2 : str
        Description of arg2
    arg3 : str
        The [JMESpath](https://jmespath.org) query.

    Returns
    -------
    bool
        Description of return value

    Raises
    ------
    AttributeError
        The ``Raises`` section is a list of all exceptions
        that are relevant to the interface.
    ValueError
        If `arg2` is equal to `arg1`.

    Examples
    --------
    Examples should be written in doctest format, and should illustrate how
    to use the function.

    >>> a=1
    >>> b=2
    >>> func(a,b)
    True

    Notes
    -----
    blabla

    """
    # doc = NumpyDocString(docstring=sample_function.__doc__)
    doc = benchmark(NumpyDocString, docstring=test_numpydoc_string.__doc__)
    assert doc["Summary"] == ["Summary line."]
    assert doc["Extended Summary"] == ["Extended description of function."]
    assert doc["Parameters"] == [
        Parameter(name="arg1", type="int, default: 5", desc=["Description of arg1"]),
        Parameter(name="arg2", type="str", desc=["Description of arg2"]),
        Parameter(
            name="arg3",
            type="str",
            desc=["The [JMESpath](https://jmespath.org) query."],
        ),
    ]
    assert doc["Returns"] == [Parameter(name="", type="bool", desc=["Description of return value"])]
    assert doc["Raises"] == [
        Parameter(
            name="",
            type="AttributeError",
            desc=[
                "The ``Raises`` section is a list of all exceptions",
                "that are relevant to the interface.",
            ],
        ),
        Parameter(name="", type="ValueError", desc=["If `arg2` is equal to `arg1`."]),
    ]
    assert doc["Examples"] == [
        "Examples should be written in doctest format, and should illustrate how",
        "to use the function.",
        "",
        ">>> a=1",
        ">>> b=2",
        ">>> func(a,b)",
        "True",
    ]
    assert doc["Notes"] == ["blabla"]
