import pytest

from jig import run


@pytest.mark.parametrize(
    "src,output",
    [
        ("loop { break }", None),
        (
            """
x := 0
loop {
  x += 1
  if x > 2 then break
}
x
""",
            3,
        ),
        (
            """
x := 0
n := 0
loop {
  x += 1
  if x < 3 then next
  n += 1
  break
}
n
""",
            1,
        ),
    ],
)
def test_loop(src, output):
    assert run(src) == output
