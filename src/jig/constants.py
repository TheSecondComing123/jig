import operator


KEYWORDS = {
    "and",
    "break",
    "else",
    "if",
    "loop",
    "next",
    "not",
    "or",
    "say",
    "then",
    "while",
}

BINARY_OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
    "**": operator.pow,
    "&": operator.and_,
    "|": operator.or_,
    "^": operator.xor,
    "<<": operator.lshift,
    ">>": operator.rshift,
}

CMP_OPS = {
    "==": operator.eq,
    "!=": operator.ne,
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
}

UNARY_OPS = {
    "+": operator.pos,
    "-": operator.neg,
    "~": operator.invert,
}
