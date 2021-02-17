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
    return " ".join([token.value for token in tokens if token.type == type_]) or None


class TreeToDict(Transformer):
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


class DocstringParser(Lark):
    """parse google style docstrings of module level python functions"""

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
            transformed = TreeToDict().transform(tree)
            return Docstring(**transformed), None
        except (GrammarError, UnexpectedCharacters, UnexpectedToken) as error:
            return None, ", ".join(error.args)
