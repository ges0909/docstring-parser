"""Parser to parse google style docstrings of module level python functions

For google style see: https://google.github.io/styleguide/pyguide.html#381-docstrings)
"""
import string
from dataclasses import dataclass
from typing import Tuple, Optional

from lark import Lark, Token
from lark import UnexpectedToken, Transformer
from lark.exceptions import UnexpectedCharacters


@dataclass
class Docstring:
    summary: Optional[str] = None
    description: Optional[str] = None
    args: Optional[list[str]] = None
    returns: Optional[str] = None
    yields: Optional[str] = None
    raises: Optional[list[str]] = None
    alias: Optional[str] = None
    examples: Optional[str] = None

    def __post_init__(self):
        self.alias = self.alias.translate({ord(c): None for c in string.whitespace})  # white space elimination
        self.alias = self.alias.casefold()  # aggressive lower case conversion


def tokens_to_str(tokens: list[Token], type_: str) -> str:
    return " ".join([token.value for token in tokens if token.type == type_]) or None


class TreeToDocstring(Transformer):
    """transforms lark trees to dicts"""

    @staticmethod
    def start(dict_list: list[dict]) -> Docstring:
        properties = {k: v for dict_ in dict_list for k, v in dict_.items()}  # reduce to single dict
        return Docstring(**properties)

    @staticmethod
    def summary(tokens: list[Token]) -> dict[str, str]:
        return {"summary": tokens_to_str(tokens, type_="WORD")}

    @staticmethod
    def description(tokens: list[Token]) -> dict[str, str]:
        return {"description": tokens_to_str(tokens, type_="WORD")}

    @staticmethod
    def args(token_lists: list[list[Token]]) -> dict[str, list[tuple[str, str, str]]]:
        return {"args": [tl for tl in token_lists if isinstance(tl, tuple)]}

    @staticmethod
    def arg(tokens: list[Token]) -> tuple[str, str, str]:
        return (
            tokens_to_str(tokens, type_="NAME"),
            tokens_to_str(tokens, type_="TYPE"),
            tokens_to_str(tokens, type_="WORD"),
        )

    @staticmethod
    def returns(tokens: list[Token]) -> dict[str, tuple[str, str]]:
        return {
            "returns": (
                tokens_to_str(tokens, type_="TYPE"),
                tokens_to_str(tokens, type_="WORD"),
            )
        }

    @staticmethod
    def yields(tokens: list[Token]) -> dict[str, tuple[str, str]]:
        return {
            "yields": (
                tokens_to_str(tokens, type_="TYPE"),
                tokens_to_str(tokens, type_="WORD"),
            )
        }

    @staticmethod
    def raises(token_lists: list[list[Token]]) -> dict[str, list[tuple]]:
        return {"raises": ([tl for tl in token_lists if isinstance(tl, tuple)])}

    @staticmethod
    def error(tokens: list[Token]) -> tuple[str, str]:
        return (
            tokens_to_str(tokens, type_="TYPE"),
            tokens_to_str(tokens, type_="WORD"),
        )

    @staticmethod
    def alias(tokens: list[Token]) -> dict[str, str]:
        return {"alias": tokens_to_str(tokens, type_="WORD")}

    @staticmethod
    def examples(tokens: list[Token]) -> dict[str, str]:
        return {"examples": tokens_to_str(tokens, type_="WORD")}


class DocstringParser(Lark):
    """parses google style docstrings of module level python functions"""

    google_grammar = r"""
    ?start:         summary? description? args? (returns | yields)? raises? alias? examples?

    summary:        _line NL
    description:    _line+ NL
    args:           "Args"     ":" NL arg+ NL
    returns:        "Returns"  ":" NL TAB _type NL
    yields:         "Yields"   ":" NL TAB _type NL
    raises:         "Raises"   ":" NL error+ NL
    examples:       "Examples" ":" NL [ ( TAB _line ) | NL ]+ NL
    alias:          "Alias"    ":" NL TAB _line NL

    arg:            TAB NAME [ SP "(" TYPE ")" ] ":" ( SP | NL ) _line+
    error:          TAB _type
    _type:          TYPE ":" ( SP | NL ) _line+
    _line:          WORD (SP WORD)* NL [ TAB TAB WORD (SP WORD)* NL ]

    NAME:           /[\*|\*\*]*[_a-zA-Z][_a-zA-Z0-9]*/
    TYPE:           /[_a-zA-Z][_a-zA-Z0-9]*/
    WORD:           /[a-zA-Z0-9.`,>=()\[\]\/:]/+
    TAB:            "    " | "  " | "\t"
    NL:             "\n"
    SP:             /[ ]/+
    """

    def __init__(self, **kwargs):
        super().__init__(
            grammar=self.google_grammar,
            parser="earley",  # supports rule priority
            **kwargs,
        )

    def parse(self, text: str, **kwargs) -> Tuple[Optional[Docstring], Optional[str]]:
        try:
            tree = super().parse(text=text, **kwargs)
            # print("\n" + tree.pretty())
            return TreeToDocstring().transform(tree), None
        except (UnexpectedCharacters, UnexpectedToken) as error:
            return None, ", ".join(error.args)
