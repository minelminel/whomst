import os
import pytest
import whomst
from . import make_path


def test_cli_parser():
    # should accept a path as argument
    pass


def test_basic_whomst():
    path = make_path("samples", "basic")
    res = whomst.look(path)
    assert set(res) == {"foo", "bar"}


def test_medium_whomst():
    path = make_path("samples", "medium")
    res = whomst.look(path)
    assert set(res) == {"bar", "foo"}


def test_hard_whomst():
    path = make_path("samples", "hard")
    res = whomst.look(path)
    assert set(res) == {"new"}


def test_complex_whomst():
    path = make_path("samples", "complex")
    res = whomst.look(path)
    assert set(res) == {"foo"}
