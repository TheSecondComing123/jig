from jig import run


def test_say(capsys):
    run("say 1")
    assert capsys.readouterr().out.splitlines() == ["1"]


def test_say_order(capsys):
    run(
        """
say 1
say -1
"""
    )
    assert capsys.readouterr().out.splitlines() == ["1", "-1"]


def test_say_returns_nothing():
    assert run("say 0") is None
