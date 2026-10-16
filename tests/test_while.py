import pytest

from jig import run


@pytest.mark.parametrize(
    "src,output",
    [
        (
            """
x := 1
while x > 0 { x -= 1 }
x
""",
            0,
        ),
        (
            """
x := 1
while 0 { x = 0 }
x
""",
            1,
        ),
        (
            """
x := 1
while x > 0 {
  z := 1
  x -= z
}
x
""",
            0,
        ),
        ("while 0 { 1 }", None),
        ("while (if 0 then 1) { 1 }", None),
    ],
)
def test_while(src, output):
    assert run(src) == output
