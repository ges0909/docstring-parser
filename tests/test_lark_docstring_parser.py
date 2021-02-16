import pytest

from src.lark_docstring_parser import DocstringParser

# param1: The [JMESpath](https://jmespath.org) query.


# @pytest.mark.repeat(1000)
def test_parse_google_style_function_docstring(benchmark):
    google_sample = r"""Summary line.

    Extended description of function.
    2nd line.
    3rd line.

    Args:
        arg1: Description of arg1
        arg2 (str): Description of arg2
        arg3: The [JMESpath](https//jmespath.org)
            query.

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

    def parse(text):
        parser = DocstringParser()
        return parser.parse(text=text)

    docstring, error = parse(text=google_sample)
    # docstring, error = benchmark(parse, text=sample)

    assert error is None, error
    assert docstring is not None

    assert docstring.summary == "Summary line."
    assert (
        docstring.description == "Extended description of function. 2nd line. 3rd line."
    )
    assert docstring.args == [
        ("arg1", "", "Description of arg1"),
        ("arg2", "str", "Description of arg2"),
        ("arg3", "", "The [JMESpath](https//jmespath.org) query."),
    ]
    assert docstring.returns == ("bool", "Description of return value")
    assert docstring.yields is None
    assert docstring.raises == [
        (
            "AttributeError",
            "The ``Raises`` section is a list of all exceptions that are relevant to the interface.",
        ),
        (
            "ValueError",
            "If `arg2` is equal to `arg1`.",
        ),
    ]
    assert docstring.alias == "what ever you want to call"
    assert (
        docstring.examples
        == "Examples should be written in doctest format, and should illustrate how to use the function."
        " >>> a=1 >>> b=2 >>> func(a,b) True"
    )
