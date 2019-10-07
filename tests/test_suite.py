import os
import pytest
import whomst


def make_path(*args):
    loc = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(loc, *args)


def test_cli_parser():
    pass


def test_basic_whomst():
    path = make_path("samples", "basic")
    res = whomst.look(path)
    assert set(res) == {"foo", "bar"}


def test_medium_whomst():
    path = make_path("samples", "medium")
    res = whomst.look(path)
    assert set(res) == {"foo"}


def test_hard_whomst():
    path = make_path("samples", "hard")
    res = whomst.look(path)
    assert set(res) == {"new"}


def test_complex_whomst():
    path = make_path("samples", "complex")
    res = whomst.look(path)
    assert set(res) == {"foo"}
