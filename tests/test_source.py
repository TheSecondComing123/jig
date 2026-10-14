import pytest

from jig import run


@pytest.mark.parametrize(
    "src",
    [
        "",
        """
""",
    ],
)
def test_empty_program(src):
    assert run(src) is None


def test_tab_whitespace():
    assert run("1\t+\t-1") == 0


def test_windows_line_endings():
    src = """
x := -1
x
"""
    assert run(src.replace("\n", "\r\n")) == -1
