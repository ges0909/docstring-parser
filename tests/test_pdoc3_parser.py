import pdoc


def function_google_style(arg1: int, arg2: str, arg3: str) -> list:
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

        >> a=1
        >> b=2
        >> func(a,b)
        True

    Alias:
        Give the function an alias name.
    """


def test_pdoc3():
    modules = ["test_pdoc3_parser"]
    context = pdoc.Context()
    modules = [pdoc.Module(mod, context=context) for mod in modules]
    pdoc.link_inheritance(context)
    #
    for m in modules:
        for f in m.functions():
            na = f.name
            mo = f.module
            ob = f.obj
            do = f.docstring
            ih = f.inherits
            fd = f.funcdef()
            pa = f.params(annotate=True)
            ra = f.return_annotation()
            pass
        html = m.html()
        pass
