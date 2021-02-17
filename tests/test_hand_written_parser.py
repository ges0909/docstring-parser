from src.hand_written_parser import parse


def test_hand_written_parser():
    """Summary line.

    Extended description of function.
    2nd line.

    Args:
        arg1: Description of arg1
        arg2 (str): Description of arg2
        arg3: The [JMESpath](https//jmespath.org) query.

    Returns:
        bool: Description of return value

    Raises:
        AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
        ValueError: If `arg2` is equal to `arg1`.

    Alias:
        what ever you want to call

    Examples:
        Examples should be written in doctest format, and should illustrate how
        to use the function.

        >>> a=1
        >>> b=2
        >>> func(a,b)
        True

    """
    docstring = parse(text=test_hand_written_parser.__doc__)
