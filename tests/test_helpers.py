import pytest
import whomst


def test_whomst_between():
    S = "from foo import bar"
    start = "from"
    end = "import"
    assert whomst.between(S, start, end) == "foo"

    S = "import foo as f"
    start = "import"
    end = "as"
    assert whomst.between(S, start, end) == "foo"

    S = "import foo.f as f"
    start = "import"
    end = "as"
    assert whomst.between(S, start, end) == "foo.f"


def test_whomst_builtinmodules():
    bim = whomst.built_in_modules()
    assert type(bim) is list

    bim = whomst.built_in_modules("list")
    assert type(bim) is list

    bim = whomst.built_in_modules("set")
    assert type(bim) is set

    bim = whomst.built_in_modules("dict")
    assert type(bim) is dict
