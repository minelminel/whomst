import os
import pytest
import whomst

# fixture
def make_path(*args):
    import os
    loc = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(loc, *args)
##

def test_whomst_terminaloutput():
    msg = ["hello", "world"]
    whomst.terminal(*msg)
    # assert whomst.terminal(msg) prints as <list>
    # assert whomst.terminal(*msg) prints as multiline <str>
    pass


def test_whomst_cli():
    p = whomst.cli(".")
    assert p == "."
    p = make_path("samples")
    assert p.split("/")[-1] == "samples"


def test_whomst_cli_error():
    path = "~/NOPE"
    # with pytest.raises(FileNotFoundError):
        # _ = whomst.cli(path)
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
    assert clean == ['bar', 'foo', 'math', 'os']


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


def test_whomst_main():
    path = "."
    whomst.main(path)
    pass


def test_whomst_entrypoint():
    import subprocess
    cmd = "python3 ../whomst/__init__.py ."
    subprocess.call(cmd, shell=True)
    pass


def test_whomst_basic():
    path = make_path("samples", "basic")
    res = whomst.look(path)
    assert set(res) == {"foo", "bar"}


def test_whomst_medium():
    path = make_path("samples", "medium")
    res = whomst.look(path)
    assert set(res) == {"bar", "foo"}


def test_whomst_hard():
    path = make_path("samples", "hard")
    res = whomst.look(path)
    assert set(res) == {"new"}


def test_whomst_complex():
    path = make_path("samples", "complex")
    res = whomst.look(path)
    assert set(res) == {"foo"}
