import pytest

from jig import run


@pytest.mark.parametrize(
    "src,output",
    [
        ("1 & 1", 1),
        ("-1 | 0", -1),
        ("-1 ^ 0", -1),
        ("~0", -1),
        ("~-1", 0),
        ("1 << 1", 2),
        ("1 >> 1", 0),
        ("1 << 1 + 0", 2),
        ("1 | 0 ^ 1 & 1", 1),
        ("1 & 1 == 1", 1),
        ("1 < 1 << 1", 1),
        ("(1 | 0) & 1", 1),
        ("0 or 1 & 1", 1),
    ],
)
def test_bitwise(src, output):
    assert run(src) == output


@pytest.mark.parametrize(
    "stmt,output",
    [("x &= 0", 0), ("x |= 0", 1), ("x <<= 1", 2), ("x >>= 1", 0), ("x ^= 1", 0)],
)
def test_bitwise_assignment(stmt, output):
    assert (
        run(
            f"""
x := 1
{stmt}
x
"""
        )
        == output
    )
