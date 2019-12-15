import os
import pytest
import whomst

def make_path(*args):
    """ Returns a path to ./tests/samples """
    loc = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(loc, *args)


def test_cli():

    with pytest.raises(SystemExit):
        whomst.cli([])

    args = whomst.cli(['.'])
    assert args.path == "."
    assert not args.skip
    assert args.verbose is False
    assert args.exhaustive is False
    assert args.all_imports is False
    del args

    args = whomst.cli(['.','-v','-a','-e'])
    assert args.verbose is True
    assert args.exhaustive is True
    assert args.all_imports is True
    del args

    args = whomst.cli(['.','-s','foo','bar'])
    assert args.skip == ['foo','bar']
    del args


def test_preflight():

    class Namespace:
        def __init__(self, **kwargs):
            self.__dict__.update(kwargs)

    base = dict(skip=[], exhaustive=False,
            all_imports=False, verbose=False)

    # cwd
    args = Namespace(path='.', **base)
    post = whomst.preflight(args)
    assert post.path == os.getcwd()
    del args, post
    # non-existant dir
    args = Namespace(path=make_path('missing'), **base)
    with pytest.raises(SystemExit):
        whomst.preflight(args)
        del args
    # dir
    args = Namespace(path=make_path('samples','basic'), **base)
    post = whomst.preflight(args)
    assert post.path == make_path('samples', 'basic')
    del args, post
    # non-existant file
    args = Namespace(path=make_path('missing.py'), **base)
    with pytest.raises(SystemExit):
        whomst.preflight(args)
        del args
    # file
    args = Namespace(path=make_path('samples','basic','__init__.py'), **base)
    post = whomst.preflight(args)
    assert post.path == make_path('samples', 'basic', '__init__.py')
    del args, post


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


def test_main_I():

    pass


def test_main_II():

    pass


def test_main_III():

    pass
