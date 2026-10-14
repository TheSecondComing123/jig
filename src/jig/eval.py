import operator

from lark import Lark, Transformer

GRAMMAR = r"""
?start: _NL? [stmt (_NL stmt)* _NL?] -> program
?stmt: NAME ":=" sum -> declare | NAME "=" sum -> assign | sum
?sum: product | sum ADD product -> binary
?product: power | product MUL power -> binary
?power: atom POW power -> binary | UNARY power -> unary | atom
?atom: NUMBER | NAME -> name | "(" sum ")"

ADD: "+" | "-"
MUL: "*" | "//" | "/" | "%"
POW: "^"
UNARY: "-"
NUMBER: /\d[\d_]*/
NAME: /[A-Za-z_]\w*/
_NL: /\n+/

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
    def __init__(self, env):
        super().__init__()
        self.env = env

    def program(self, stmts):
        return stmts[-1]

    def declare(self, args):
        name, value = args
        self.env[name] = value

    def assign(self, args):
        name, value = args
        self.env[name] = value

    def name(self, args):
        name = args[0]
        return self.env[name]

    def NUMBER(self, tok):
        return int(tok.replace("_", ""))

    def binary(self, args):
        left, op, right = args
        return BINARY_OPS[op](left, right)

    def unary(self, args):
        op, operand = args
        return UNARY_OPS[op](operand)


def evaluate(src, env=None):
    if env is None:
        env = {}
    return Evaluator(env).transform(parser.parse(src))
