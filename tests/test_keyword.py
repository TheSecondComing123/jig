import pytest

from jig import run


@pytest.mark.parametrize(
    "name",
    ["if", "then", "else", "while", "and", "or", "not", "break", "next", "say"],
)
def test_keyword_is_not_a_name(name):
    with pytest.raises(Exception, match="Unexpected"):
        run(f"{name} := 1")
