import pytest

from jig import run


@pytest.mark.parametrize(
    "src,output",
    [
        ("1 == 1", 1),
        ("1 != 1", 0),
        ("0 < 1", 1),
        ("1 <= 0", 0),
        ("1 > 0", 1),
        ("0 >= 1", 0),
        ("1 >= 1", 1),
        ("1 + 0 == 1", 1),
        ("-1 < 0 < 1", 1),
        ("-1 < 0 < 0", 0),
        ("1 < 0 < 1 // 0", 0),
        ("-1 < 0 < 1 < 1", 0),
        ("0 < 1 < 1 < 1 // 0", 0),
    ],
)
def test_compare(src, output):
    assert run(src) == output
