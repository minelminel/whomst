import whomst

def test_cli():
    _input = ['.', '--verbose', '--skip', 'foo', 'bar']
    args = whomst.cli(_input)
    assert args


def test_logging():
    pass


def test_preflight():
    pass


def test_make_exclusions():
    pass


def test_walk_files():
    pass


def test_read_imports():
    pass


def test_clean_lines():
    pass


def test_ignore_included():
    pass


def test_terminal():
    pass
