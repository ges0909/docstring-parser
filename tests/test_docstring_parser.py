from docstring_parser import parse

numpy_sample = r"""
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


def test_docstring_parser():
    doc = parse(numpy_sample)
    assert doc.short_description == "Summary line."
    assert doc.long_description == "Extended description of function."

    assert doc.params[0].arg_name == "arg1"
    assert doc.params[0].type_name == "int, default: 5"
    assert doc.params[0].description == "Description of arg1"

    assert doc.params[1].arg_name == "arg2"
    assert doc.params[1].type_name == "str"
    assert doc.params[1].description == "Description of arg2"

    assert doc.params[2].arg_name == "arg3"
    assert doc.params[2].type_name == "str"
    assert doc.params[2].description == "The [JMESpath](https://jmespath.org) query."

    assert doc.returns.type_name == "bool"
    assert doc.returns.description == "Description of return value"

    assert doc.raises[0].type_name == "AttributeError"
    assert doc.raises[1].type_name == "ValueError"

    examples = [meta for meta in doc.meta for args in meta.args if args == "examples"]
    assert examples[0].args == ["examples"]
    # assert examples[0].description == "..."

    notes = [meta for meta in doc.meta for args in meta.args if args == "notes"]
    assert notes[0].args == ["notes"]
    assert notes[0].description == "blabla"