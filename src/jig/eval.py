import operator

from lark import Lark, Transformer

parser = Lark.open("grammar.lark", rel_to=__file__)

BINARY_OPS = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "/": operator.truediv,
    "//": operator.floordiv,
    "%": operator.mod,
    "^": operator.pow,
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
    "-": operator.neg,
}


class Evaluator(Transformer):
    def __init__(self, env):
        super().__init__()
        self.env = env

    def program(self, stmts):
        return stmts[-1]

    def say(self, args):
        print(args[0])

    def declare(self, args):
        name, value = args
        self.env[name] = value

    def assign(self, args):
        name, value = args
        self.env[name] = value

    def augset(self, args):
        name, op, value = args
        self.env[name] = BINARY_OPS[op[:-1]](self.env[name], value)

    def name(self, args):
        name = args[0]
        return self.env[name]

    def NUMBER(self, tok):
        return int(tok.replace("_", ""))

    def binary(self, args):
        left, op, right = args
        return BINARY_OPS[op](left, right)

    def compare(self, args):
        left = args[0]
        for i in range(1, len(args), 2):
            op = args[i]
            right = args[i + 1]
            if not CMP_OPS[op](left, right):
                return 0
            left = right
        return 1

    def unary(self, args):
        op, operand = args
        return UNARY_OPS[op](operand)


def evaluate(src, env=None):
    if env is None:
        env = {}
    return Evaluator(env).transform(parser.parse(src))
