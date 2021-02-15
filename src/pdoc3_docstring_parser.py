import inspect
import re
import textwrap


def _is_indented_4_spaces(txt, _3_spaces_or_less=re.compile(r"\n\s{0,3}\S").search):
    return "\n" not in txt or not _3_spaces_or_less(txt)


def _fix_indent(name, type, desc):
    """Maybe fix indent from 2 to 4 spaces."""
    if not _is_indented_4_spaces(desc):
        desc = desc.replace("\n", "\n  ")
    return name, type, desc


def _deflist(name, type, desc):
    """
    Returns `name`, `type`, and `desc` formatted as a
    Python-Markdown definition list entry. See also:
    https://python-markdown.github.io/extensions/definition_lists/
    """
    # Wrap any identifiers and string literals in parameter type spec
    # in backticks while skipping common "stopwords" such as 'or', 'of',
    # 'optional' ... See §4 Parameters:
    # https://numpydoc.readthedocs.io/en/latest/format.html#sections
    type_parts = re.split(
        r"( *(?: of | or |, *default(?:=|\b)|, *optional\b) *)", type or ""
    )
    type_parts[::2] = [f"`{s}`" if s else s for s in type_parts[::2]]
    type = "".join(type_parts)

    desc = desc or "&nbsp;"
    assert _is_indented_4_spaces(desc)
    assert name or type
    ret = ""
    if name:
        # NOTE: Triple-backtick argument names so we skip linkifying them
        ret += f"**```{name.replace(', ', '```**, **```')}```**"
    if type:
        ret += f" :&ensp;{type}" if ret else type
    ret += f"\n:   {desc}\n\n"
    return ret


def google(text):
    """
    Convert `text` in Google-style docstring format to Markdown
    to be further converted later.
    """

    def googledoc_sections(match):
        section, body = match.groups("")
        if not body:
            return match.group()
        body = textwrap.dedent(body)
        section = section.title()
        if section in ("Args", "Attributes"):
            body = re.compile(
                r"^([\w*]+)(?: \(([\w.,=\[\] -]+)\))?: "
                r"((?:.*)(?:\n(?: {2,}.*|$))*)",
                re.MULTILINE,
            ).sub(
                lambda m: _deflist(*_fix_indent(*m.groups())),
                inspect.cleandoc("\n" + body),
            )
        elif section in ("Returns", "Yields", "Raises", "Warns"):
            body = re.compile(
                r"^()([\w.,\[\] ]+): " r"((?:.*)(?:\n(?: {2,}.*|$))*)", re.MULTILINE
            ).sub(
                lambda m: _deflist(*_fix_indent(*m.groups())),
                inspect.cleandoc("\n" + body),
            )
        # Convert into markdown sections. End underlines with '='
        # to avoid matching and re-processing as Numpy sections.
        return f"\n{section}\n-----=\n{body}"

    text = re.compile(r"^([A-Z]\w+):$\n" r"((?:\n?(?: {2,}.*|$))+)", re.MULTILINE).sub(
        googledoc_sections, text
    )
    return text
