import pytest
from lark.exceptions import UnexpectedInput

from jig import run


@pytest.mark.parametrize(
    "src,expected",
    [
        ('"hi"', "hi"),
        ('""', ""),
        ('"{1}"', "1"),
        ('"x{0}y"', "x0y"),
        ('"{"ok"}"', "ok"),
        ('"{ {1} }"', "1"),
        ('"{if 1 then { "ok" } else "no"}"', "ok"),
        ('"a" == "a"', 1),
        ('"a" < "b"', 1),
        ('"{if 1 then 0 else 1}"', "0"),
        ('"a}b"', "a}b"),
        ('"" or "anon"', "anon"),
        ('not ""', 1),
        ('if "" then 1 else 2', 2),
        ('if "a" then 1 else 2', 1),
    ],
)
def test_text(src, expected):
    assert run(src) == expected


@pytest.mark.parametrize(
    "src",
    [
        '"a" + "b"',
        's := "a"; s += "b"',
        '1 == "1"',
    ],
)
def test_text_errors(src):
    with pytest.raises(TypeError):
        run(src)


@pytest.mark.parametrize("src", ['"a', r'"\n"', '"{1"', '"{}"'])
def test_bad_text(src):
    with pytest.raises(UnexpectedInput):
        run(src)


def test_say_text(capsys):
    run('say "hi"')
    assert capsys.readouterr().out == "hi\n"
