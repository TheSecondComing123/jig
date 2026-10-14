import pytest
from lark.exceptions import VisitError

from jig import run


@pytest.mark.parametrize(
    "src,output",
    [
        ("1 + -1", 0),
        ("0 - 1", -1),
        ("-1 * -1", 1),
        ("1 / -1", -1),
        ("1 // -1", -1),
        ("-1 % 1", 0),
        ("-1 ^ 0", -1),
        ("0 ^ 1 ^ 0", 0),
        ("1 + 0 * -1", 1),
        ("(1 + 0) * -1", -1),
        ("1_0 - 1_0", 0),
    ],
)
def test_arith(src, output):
    assert run(src) == output


@pytest.mark.parametrize("src", ["1 / 0", "1 // 0", "1 % 0"])
def test_zero_division(src):
    with pytest.raises(VisitError):
        run(src)


def test_syntax_error():
    with pytest.raises(Exception, match="Unexpected"):
        run("1 +")
