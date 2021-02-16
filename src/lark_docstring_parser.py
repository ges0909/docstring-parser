import logging
from collections import ChainMap
from dataclasses import dataclass
from typing import Tuple, Optional, Union

from lark import Lark, logger, Token
from lark import UnexpectedToken, Transformer
from lark.exceptions import UnexpectedCharacters, GrammarError

logger.setLevel(logging.DEBUG)


@dataclass()
class Docstring:
    summary: Optional[str] = None
    description: Optional[str] = None
    args: Optional[list[str]] = None
    returns: Optional[str] = None
    yields: Optional[str] = None
    raises: Optional[list[str]] = None
    alias: Optional[str] = None
    examples: Optional[str] = None


def words_to_str(tokens: list[Token], type_: str) -> str:
    return " ".join([token.value for token in tokens if token.type == type_])


class DocstringTransformer(Transformer):
    @staticmethod
    def start(children: list[dict]) -> dict[str, Union[str, tuple]]:
        return dict(ChainMap(*children[::-1]))  # reduce list of dicts to single dict

    @staticmethod
    def summary(tokens: list[Token]) -> dict[str, str]:
        return {"summary": words_to_str(tokens, type_="WORD")}

    @staticmethod
    def description(tokens: list[Token]) -> dict[str, str]:
        return {"description": words_to_str(tokens, type_="WORD")}

    @staticmethod
    def args(token_lists: list[list[Token]]) -> dict[str, list[tuple[str, str, str]]]:
        return {"args": [tl for tl in token_lists if isinstance(tl, tuple)]}

    @staticmethod
    def arg(tokens: list[Token]) -> tuple[str, str, str]:
        return (
            words_to_str(tokens, type_="NAME"),
            words_to_str(tokens, type_="TYPE"),
            words_to_str(tokens, type_="WORD"),
        )

    @staticmethod
    def returns(tokens: list[Token]) -> dict[str, tuple[str, str]]:
        return {
            "returns": (
                words_to_str(tokens, type_="TYPE"),
                words_to_str(tokens, type_="WORD"),
            )
        }

    @staticmethod
    def yields(tokens: list[Token]) -> dict[str, tuple[str, str]]:
        return {
            "yields": (
                words_to_str(tokens, type_="TYPE"),
                words_to_str(tokens, type_="WORD"),
            )
        }

    @staticmethod
    def raises(token_lists: list[list[Token]]) -> dict[str, list[tuple]]:
        return {"raises": ([tl for tl in token_lists if isinstance(tl, tuple)])}

    @staticmethod
    def error(tokens: list[Token]) -> tuple[str, str]:
        return (
            words_to_str(tokens, type_="TYPE"),
            words_to_str(tokens, type_="WORD"),
        )

    @staticmethod
    def alias(tokens: list[Token]) -> dict[str, str]:
        return {"alias": words_to_str(tokens, type_="WORD")}

    @staticmethod
    def examples(tokens: list[Token]) -> dict[str, str]:
        return {"examples": words_to_str(tokens, type_="WORD")}


# https://google.github.io/styleguide/pyguide.html#381-docstrings) definitions

# A docstring should be organized as a summary line (one physical line not exceeding 80 characters)
# terminated by a period, question mark, or exclamation point. When writing more (encouraged), this
# must be followed by a blank line, followed by the rest of the docstring starting at the same cursor
# position as the first quote of the first line.

# Certain aspects of a function should be documented in special sections, listed below. Each section
# begins with a heading line, which ends with a colon. All sections other than the heading should
# maintain a hanging indent of two or four spaces (be consistent within a file). These sections can
# be omitted in cases where the function’s name and signature are informative enough that it can be
# aptly described using a one-line docstring.

# Args:
# List each parameter by name. A description should follow the name, and be separated by a colon
# followed by either a space or newline. If the description is too long to fit on a single 80-character
# line, use a hanging indent of 2 or 4 spaces more than the parameter name (be consistent with the
# rest of the docstrings in the file). The description should include required type(s) if the code
# does not contain a corresponding type annotation. If a function accepts *foo (variable length
# argument lists) and/or **bar (arbitrary keyword arguments), they should be listed as *foo and **bar.

# Returns: (or Yields: for generators)
# Describe the type and semantics of the return value. If the function only returns None, this section
# is not required. It may also be omitted if the docstring starts with Returns or Yields (e.g. """Returns
# row from Bigtable as a tuple of strings.""") and the opening sentence is sufficient to describe return value.

# Raises:
# List all exceptions that are relevant to the interface followed by a description. Use a similar
# exception name + colon + space or newline and hanging indent style as described in Args:. You
# should not document exceptions that get raised if the API specified in the docstring is violated
# (because this would paradoxically make behavior under violation of the API part of the API).


class DocstringParser(Lark):
    """parse google style docstrings of module level python functions"""

    grammar = r"""
    ?start:         summary description? args? (returns | yields)? raises? alias? examples?

    summary:        _line _nl
    description:    _line+ _nl
    args:           "Args"     ":" _nl arg+ _nl
    returns:        "Returns"  ":" _nl _type _nl
    yields:         "Yields"   ":" _nl TYPE ":" _type _nl
    raises:         "Raises"   ":" _nl error+ _nl
    alias:          "Alias"    ":" _nl _line _nl
    examples:       "Examples" ":" _nl [ _line | _nl ]+ _nl
    
    arg:            NAME [ "(" TYPE ")" ] ":" _line+
    error:          _type
    _type:          TYPE ":" _line+
    _line:          WORD+ _nl
    _nl:            "\n"
    
    NAME:           /[_a-zA-Z][_a-zA-Z0-9]*/
    TYPE:           /[_a-zA-Z][_a-zA-Z0-9]*/
    WORD:           /[a-zA-Z0-9.`,>=()\[\]\/]/+
    TAB:            "\t"
    SP:             /[ ]/+
    
    %ignore         SP
    """

    def __init__(self, **kwargs):
        super().__init__(
            grammar=self.grammar,
            parser="earley",  # supports rule priority
            # parser="lalr",  # supports terminal priority
            # ambiguity="explicit",
            # lexer="dynamic_complete",
            **kwargs,
        )

    def parse(self, text: str, **kwargs) -> Tuple[Optional[Docstring], Optional[str]]:
        try:
            tree = super().parse(text=text, **kwargs)
            # print("\n" + tree.pretty())
            transformed = DocstringTransformer().transform(tree)
            return Docstring(**transformed), None
        except (GrammarError, UnexpectedCharacters, UnexpectedToken) as error:
            return None, ", ".join(error.args)
