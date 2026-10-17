import pytest

from jig import run


@pytest.mark.parametrize(
    "src,output",
    [
        (
            """
x := 0
while 1 {
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
while x < 3 {
  x += 1
  if x == 2 then next
  n += 1
}
n
""",
            2,
        ),
        (
            """
x := 0
while 1 {
  while 1 { break }
  x += 1
  if x > 1 then break
}
x
""",
            2,
        ),
        ("while 1 { break }", None),
        (
            """
x := 0
while 1 {
  y := 1
  x += y
  break
}
y := 5
x + y
""",
            6,
        ),
    ],
)
def test_break_and_next(src, output):
    assert run(src) == output


@pytest.mark.parametrize(
    "src", ["break", "next", "if 0 then break", "while 1 { 1 }; next"]
)
def test_outside_a_loop(src):
    with pytest.raises(SyntaxError, match="outside a loop"):
        run(src)
