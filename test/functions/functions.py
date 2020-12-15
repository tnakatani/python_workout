import pytest

from src.functions.functions import *


################################################################################
# XML Generator


def test_single_tag():
    assert myxml("foo") == "<foo></foo>"


def test_single_tag_and_content():
    assert myxml("foo", "bar") == "<foo>bar</foo>"


def test_single_tag_content_and_attributes():
    assert myxml("foo", "bar", a=1, b=2, c=3) == "<foo a=1 b=2 c=3>bar</foo>"


################################################################################
# Factorial


def test_no_nums():
    assert factorial() == 1


def test_two_nums():
    assert factorial(1, 2) == 2


def test_three_nums():
    assert factorial(1, 2, 3) == 6
