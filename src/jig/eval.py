import operator
from contextlib import contextmanager

from lark import Lark, Tree
from lark.visitors import Interpreter, visit_children_decor

parser = Lark.open("grammar.lark", rel_to=__file__, parser="lalr", lexer="basic")

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


class Break(Exception):
    pass


class Next(Exception):
    pass


def truthy(value):
    return value is not None and value != 0


class Env:
    def __init__(self, parent=None, vars=None):
        self.parent = parent
        self.vars = {} if vars is None else vars

    def owner(self, name):
        env = self
        while env:
            if name in env.vars:
                return env
            env = env.parent

    def existing(self, name):
        env = self.owner(name)
        if env is None:
            raise NameError(f"undefined name `{name}`")
        return env.vars

    def get(self, name):
        return self.existing(name)[name]

    def set(self, name, value):
        self.existing(name)[name] = value

    def declare(self, name, value):
        if self.owner(name):
            raise NameError(f"`{name}` is already defined")
        self.vars[name] = value


class Evaluator(Interpreter):
    def __init__(self, env):
        self.env = env

    @contextmanager
    def scope(self):
        saved = self.env
        self.env = Env(saved)
        try:
            yield
        finally:
            self.env = saved

    @visit_children_decor
    def program(self, stmts):
        return stmts[-1]

    @visit_children_decor
    def say(self, args):
        print(args[0])

    @visit_children_decor
    def declare(self, args):
        name, value = args
        self.env.declare(name, value)

    @visit_children_decor
    def assign(self, args):
        name, value = args
        self.env.set(name, value)

    def augset(self, tree):
        name, op, value = tree.children
        old = self.env.get(name)
        self.env.set(name, BINARY_OPS[op[:-1]](old, self.visit(value)))

    @visit_children_decor
    def name(self, args):
        return self.env.get(args[0])

    def if_then(self, tree):
        cond, then, other = tree.children
        if truthy(self.visit(cond)):
            return self.visit(then)
        return self.visit(other) if other else None

    def or_op(self, tree):
        left, right = tree.children
        value = self.visit(left)
        return value if truthy(value) else self.visit(right)

    def and_op(self, tree):
        left, right = tree.children
        value = self.visit(left)
        return self.visit(right) if truthy(value) else value

    def not_op(self, tree):
        return int(not truthy(self.visit(tree.children[0])))

    def block(self, tree):
        value = None
        with self.scope():
            for stmt in tree.children:
                if stmt:
                    value = self.visit(stmt)
        return value

    def while_block(self, tree):
        *cond, body = tree.children
        while not cond or truthy(self.visit(cond[0])):
            try:
                self.visit(body)
            except Break:
                break
            except Next:
                pass

    def break_(self, tree):
        raise Break

    def next_(self, tree):
        raise Next

    @visit_children_decor
    def num(self, args):
        return int(args[0].replace("_", ""))

    @visit_children_decor
    def binary(self, args):
        left, op, right = args
        return BINARY_OPS[op](left, right)

    @visit_children_decor
    def compare(self, args):
        left = args[0]
        for i in range(1, len(args), 2):
            op = args[i]
            right = args[i + 1]
            if not CMP_OPS[op](left, right):
                return 0
            left = right
        return 1

    @visit_children_decor
    def unary(self, args):
        op, operand = args
        return UNARY_OPS[op](operand)


def check_loops(tree, in_loop=False):
    if tree.data in ("break_", "next_") and not in_loop:
        raise SyntaxError(f"`{tree.data[:-1]}` outside a loop")
    for child in tree.children:
        if isinstance(child, Tree):
            check_loops(child, in_loop or tree.data == "while_block")


def evaluate(src, env=None):
    if env is None:
        env = {}
    tree = parser.parse(src)
    check_loops(tree)
    return Evaluator(Env(vars=env)).visit(tree)
