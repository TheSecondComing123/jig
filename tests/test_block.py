import pytest

from jig import run


@pytest.mark.parametrize(
    "src,output",
    [
        (
            """
{
  1
  -1
}
""",
            -1,
        ),
        ("{}", None),
        (
            """
x := {
  1
  -1
}
x
""",
            -1,
        ),
        (
            """
x := 1
{ x = -1 }
x
""",
            -1,
        ),
    ],
)
def test_block(src, output):
    assert run(src) == output


@pytest.mark.parametrize(
    "src",
    [
        """
{ y := 1 }
y
""",
        """
x := 1
{ x := 0 }
""",
    ],
)
def test_scope_error(src):
    with pytest.raises(NameError):
        run(src)
