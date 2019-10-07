import pytest
import os
import whomst
from . import make_path


def test_terminaloutput():
    msg = ["hello", "world"]
    # assert whomst.terminal(msg) prints as <list>
    # assert whomst.terminal(*msg) prints as multiline <str>
    pass


def test_whomst_look():
    path = make_path("samples")
    ready = whomst.look(path)
    assert ready == ['bar', 'foo', 'new']


def test_whomst_ignoreincluded():
    clean = {'bar', 'foo', 'math', 'os'}
    ready = whomst.ignore_included(clean)
    assert ready == ['bar', 'foo']


def test_whomst_cleanlines():
    cursor = {'import foo', 'import foo, bar', 'import math.floor', 'import os'}
    clean = whomst.clean_lines(cursor)
    assert clean == {'bar', 'foo', 'math', 'os'}


def test_whomst_readimports():
    abs_path = make_path("samples", "basic", "__init__.py")
    file_data = whomst.read_imports(abs_path)
    assert file_data == {'import foo', 'import foo, bar', 'import math.floor', 'import os'}


def test_whomst_walk_files():
    path = make_path("samples")
    exclude = {"complex", "hard", "medium"}
    for _ in whomst.walk_files(path, exclude):
        assert os.path.exists(_)
        assert [x not in _ for x in exclude]


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
    bim = whomst.built_in_modules("list")
    assert type(bim) is list

    bim = whomst.built_in_modules("set")
    assert type(bim) is set

    bim = whomst.built_in_modules("dict")
    assert type(bim) is dict
