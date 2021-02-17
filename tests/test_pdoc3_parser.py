from src.pdoc3_docstring_parser import google


def test_numpy_style():
    """Summary line.

    Extended description of function.

    Args:
        arg1 (int, default 5): Description of arg1
        arg2 (str): Description of arg2
        arg3 (str): The [JMESpath](https://jmespath.org) query.

    Returns:
        bool: Description of return value

    Raises:
        AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
        ValueError: If `arg2` is equal to `arg1`.

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> a=1
        >>> b=2
        >>> func(a,b)
        True

    """

    markdown = google(test_numpy_style.__doc__)
