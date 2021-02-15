from collections import ChainMap
from dataclasses import dataclass
from typing import Tuple, Optional, Union

from lark import Lark, UnexpectedToken, Transformer
from lark.exceptions import UnexpectedCharacters, GrammarError


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


class DocstringTransformer(Transformer):
    @staticmethod
    def words_to_str(tokens, type_: str) -> str:
        return " ".join([token.value for token in tokens if token.type == type_])

    @staticmethod
    def start(
        children: list,
    ) -> dict[str, Union[str, tuple[str, str], tuple[str, str, str]]]:
        return dict(ChainMap(*children[::-1]))  # reduce list of dicts to single dict

    def summary(self, tokens: list) -> dict[str, str]:
        return {"summary": self.words_to_str(tokens, type_="WORD")}

    def description(self, tokens: list) -> dict[str, str]:
        return {"description": self.words_to_str(tokens, type_="WORD")}

    @staticmethod
    def args(children: list) -> dict[str, list[tuple[str, str, str]]]:
        return {"args": [child for child in children if isinstance(child, tuple)]}

    def arg(self, tokens: list) -> tuple[str, str, str]:
        return (
            self.words_to_str(tokens, type_="NAME"),
            self.words_to_str(tokens, type_="TYPE"),
            self.words_to_str(tokens, type_="WORD"),
        )

    def returns(self, tokens: list) -> dict[str, tuple[str, str]]:
        return {
            "returns": (
                self.words_to_str(tokens, type_="TYPE"),
                self.words_to_str(tokens, type_="WORD"),
            )
        }

    def yields(self, tokens: list) -> dict[str, tuple[str, str]]:
        return {
            "yields": (
                self.words_to_str(tokens, type_="TYPE"),
                self.words_to_str(tokens, type_="WORD"),
            )
        }

    @staticmethod
    def raises(children: list) -> dict[str, list[tuple[str, str]]]:
        return {"raises": [child for child in children if isinstance(child, tuple)]}

    def error(self, tokens: list) -> tuple[str, str]:
        return (
            self.words_to_str(tokens, type_="TYPE"),
            self.words_to_str(tokens, type_="WORD"),
        )

    def alias(self, tokens: list) -> dict[str, str]:
        return {"alias": self.words_to_str(tokens, type_="WORD")}

    def examples(self, tokens: list) -> dict[str, str]:
        return {"examples": self.words_to_str(tokens, type_="WORD")}


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
    ?start:         summary description args (returns | yields)? raises? alias? examples?

    summary:        WORD+ NL NL
    description:    [ [ WORD+ NL ]+ NL ]*
    args:           [ _ARGS COLON NL arg+ ]
    returns:        _RETURNS COLON NL TYPE COLON WORD+
    yields:         _YIELDS COLON NL TYPE COLON WORD+
    raises:         _RAISES COLON NL error+
    alias:          _ALIAS COLON NL WORD+
    examples:       _EXAMPLES COLON NL WORD+
    
    arg:            TAB NAME COLON (NL | SP) [WORD+ NL]+
                  | TAB NAME BRACKET_OPEN TYPE BRACKET_CLOSE COLON (NL | SP) [WORD+ NL]+
                  
    error:          TAB TYPE COLON [WORD+ NL]+
    
    _ARGS:          "Args"
    _RETURNS:       "Returns"
    _YIELDS:        "Yields"
    _RAISES:        "Raises"
    _ALIAS:         "Alias"
    _EXAMPLES:      "Examples"
    
    NAME:           /[a-zA-Z][a-zA-Z0-9_]*/
    TYPE:           /[a-zA-Z][a-zA-Z0-9_]*/
    COLON:          ":"
    BRACKET_OPEN:   "("
    BRACKET_CLOSE:  ")"
    WORD:           /[a-zA-Z0-9.`,>=()\[\]\/]+/

    NL:             "\n"
    SP:             " "
    TAB:            ("  " | "    " | "\t")
    
    WS:             /\s+/
    
    %ignore         WS
    """

    def __init__(self, **kwargs):
        super().__init__(
            grammar=self.grammar,
            parser="earley",  # supports rule priority
            # parser="lalr",  # supports terminal priority
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
