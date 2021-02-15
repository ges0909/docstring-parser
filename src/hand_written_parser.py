from typing import NamedTuple


class Docstring(NamedTuple):
    summary: str
    description: str
    args: list[str]
    returns: str
    yields: str
    raises: list[str]
    alias: str
    examples: str


def parse(text: str) -> Docstring:
    words = text.split(r"\s+")
    for line in words:
        pass
