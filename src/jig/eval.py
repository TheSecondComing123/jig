import operator

from lark import Lark, Transformer

GRAMMAR = r"""
?start: sum
?sum: product | sum ADD product -> binary
?product: power | product MUL power -> binary
?power: atom POW power -> binary | UNARY power -> unary | atom
?atom: NUMBER | "(" sum ")"

ADD: "+" | "-"
MUL: "*" | "//" | "/" | "%"
POW: "^"
UNARY: "-"
NUMBER: /\d[\d_]*/

%ignore /[ \t\r]+/
"""

parser = Lark(GRAMMAR)

BINARY_OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
    "^": operator.pow,
}

UNARY_OPS = {
    "-": operator.neg,
}


class Evaluator(Transformer):
    def NUMBER(self, tok):
        return int(tok.replace("_", ""))

    def binary(self, args):
        left, op, right = args
        return BINARY_OPS[op](left, right)

    def unary(self, args):
        op, operand = args
        return UNARY_OPS[op](operand)


def evaluate(src):
    return Evaluator().transform(parser.parse(src))
