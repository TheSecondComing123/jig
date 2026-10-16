import pytest

from jig import run


@pytest.mark.parametrize(
    "src,output",
    [
        ("if 1 then -1 else 0", -1),
        ("if 0 then 1 else -1", -1),
        ("if 0 then 1", None),
        ("if (if 0 then 1) then 1 else -1", -1),
        ("if 1 > 0 then 1 else 0", 1),
        ("if 1 then 1 else 1 / 0", 1),
        ("if 0 then 1 else if 1 then -1 else 0", -1),
        ("1 + (if 1 then 1 else 0)", 2),
    ],
)
def test_if(src, output):
    assert run(src) == output


def test_if_value():
    assert (
        run(
            """
x := if 0 then 1 else -1
x
"""
        )
        == -1
    )


def test_keyword_prefix_is_a_name():
    assert (
        run(
            """
iffy := 1
iffy
"""
        )
        == 1
    )
