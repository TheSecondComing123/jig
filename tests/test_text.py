import pytest

from jig import run


@pytest.mark.parametrize(
    "src,expected",
    [
        ('"hi"', "hi"),
        ('""', ""),
        ('"a" == "a"', 1),
        ('"a" < "b"', 1),
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


@pytest.mark.parametrize("src", ['"a', r'"\n"', '"{x}"'])
def test_bad_text(src):
    with pytest.raises(Exception, match="No terminal matches"):
        run(src)


def test_say_text(capsys):
    run('say "hi"')
    assert capsys.readouterr().out == "hi\n"
