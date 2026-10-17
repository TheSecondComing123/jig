import pytest

from jig import run


@pytest.mark.parametrize(
    "src,output",
    [
        ("1 and 0", 0),
        ("1 and -1", -1),
        ("0 and 1 / 0", 0),
        ("0 or -1", -1),
        ("1 or 1 / 0", 1),
        ("not 0", 1),
        ("not -1", 0),
        ("not 0 == 0", 0),
        ("1 or 0 and 0", 1),
        ("{} or -1", -1),
        ("{} and 1", None),
        ("if 1 and 0 then 1 else -1", -1),
    ],
)
def test_logic(src, output):
    assert run(src) == output


def test_keyword_prefix_is_a_name():
    src = """
order := 1
order
"""
    assert run(src) == 1
