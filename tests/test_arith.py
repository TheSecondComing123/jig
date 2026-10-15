import pytest

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


@pytest.mark.parametrize(
    "op,output", [("+=", 0), ("-=", 2), ("*=", -1), ("/=", -1), ("//=", -1), ("%=", 0)]
)
def test_augmented_assignment(op, output):
    assert (
        run(
            f"""
x := 1
x {op} -1
x
"""
        )
        == output
    )


def test_variables():
    assert (
        run(
            """
x := 1
x = -1
x
"""
        )
        == -1
    )


@pytest.mark.parametrize("src", ["1 / 0", "1 // 0", "1 % 0"])
def test_zero_division(src):
    with pytest.raises(ZeroDivisionError):
        run(src)


def test_syntax_error():
    with pytest.raises(Exception, match="Unexpected"):
        run("1 +")
