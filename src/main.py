import logging as l
import typing
import enum
from enum import Enum
from typing import List, Tuple, Optional

# Import reduce from functools
from functools import reduce

l.basicConfig(level=l.DEBUG)


class NormalString(str):
    def __repr__(self):
        return f"NormalString({super().__repr__()})"


class Token(Enum):
    OPEN_PAREN = "("
    CLOSE_PAREN = ")"
    ADD = "+"
    MULT = "*"
    INT = "INT"


class TokVal:
    def __init__(self, tok: Token, val: Optional[int] = None):
        self.tok = tok
        self.val = val

    def __repr__(self):
        return f"TokVal({self.tok}, {self.val})"


def compose(f, g):
    # Debug the input and output of f and g and then return the composition of f and g
    def h(x):
        l.debug(f"Input: {x}")
        y = f(x)
        l.debug(f"Output: {y}")
        return g(y)

    return h


def compose_reduce(*fs):
    return reduce(compose, fs)


def normalize(s: str) -> NormalString:
    return s.replace("(", " ( ").replace(")", " ) ")


def split_whitespace(string: NormalString) -> List[str]:
    return string.split()


def tokenize_list(s: List[NormalString]) -> List[TokVal]:
    return [tokenize(x) for x in s]


def tokenize(s: NormalString) -> TokVal:
    match s:
        case "(":
            return TokVal(Token.OPEN_PAREN)
        case ")":
            return TokVal(Token.CLOSE_PAREN)
        case "+":
            return TokVal(Token.ADD)
        case "*":
            return TokVal(Token.MULT)
        case _:
            return TokVal(Token.INT, int(str(s)))


if __name__ == "__main__":
    l.info("Starting main.py")
    # Compose list of functions
    funcs = [
        normalize,
        split_whitespace,
        tokenize_list,
    ]
    # Compose functions
    composed = compose_reduce(*funcs)
    example = "(+ 1 2)"
    # Call composed function
    composed(example)

    l.info("Finished main.py")
