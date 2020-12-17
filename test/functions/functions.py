import string
import random
import pytest

from src.functions.functions import *


################################################################################
# XML Generator


def test_single_tag():
    assert myxml("foo") == "<foo></foo>"


def test_single_tag_and_content():
    assert myxml("foo", "bar") == "<foo>bar</foo>"


def test_single_tag_content_and_attributes():
    assert myxml("foo", "bar", a=1, b=2, c=3) == '<foo a="1" b="2" c="3">bar</foo>'


def test_nested():
    assert myxml("a", myxml("b", myxml("c", "text"))) == "<a><b><c>text</c></b></a>"


def test_attributes():
    assert myxml("tagname", a=1, b=2, c=3) == '<tagname a="1" b="2" c="3"></tagname>'


def test_attributes_and_text():
    assert (
        myxml("tagname", "text", a=1, b=2, c=3)
        == '<tagname a="1" b="2" c="3">text</tagname>'
    )


################################################################################
# Factorial


def test_no_nums():
    assert factorial() == 1


def test_two_nums():
    assert factorial(1, 2) == 2


def test_three_nums():
    assert factorial(1, 2, 3) == 6


################################################################################
# Prefix Notation Calculator


@pytest.mark.parametrize(
    "inputs, expected",
    [
        ("+12", 3),
        ("+123", 6),
        ("+1234", 10),
    ],
)
def test_addition(inputs, expected):
    assert calc(inputs) == expected


@pytest.mark.parametrize(
    "inputs, expected",
    [
        ("-12", -1),
        ("-123", -4),
        ("-1234", -8),
    ],
)
def test_subtraction(inputs, expected):
    assert calc(inputs) == expected


@pytest.mark.parametrize(
    "inputs, expected",
    [
        ("*12", 2),
        ("*123", 6),
        ("*1234", 24),
    ],
)
def test_multiplication(inputs, expected):
    assert calc(inputs) == expected


@pytest.mark.parametrize(
    "inputs, expected",
    [
        ("/12", 0.5),
        ("/124", 0.125),
        ("/1248", 0.015625),
    ],
)
def test_division(inputs, expected):
    assert calc(inputs) == expected


@pytest.mark.parametrize(
    "inputs, expected",
    [
        ("%12", 1),
        ("%123", 1),
        ("%1234", 1),
    ],
)
def test_modulo(inputs, expected):
    assert calc(inputs) == expected


@pytest.mark.parametrize(
    "inputs, expected",
    [
        ("**12", 1),
        ("**123", 1),
        ("**1234", 1),
    ],
)
def test_exponential(inputs, expected):
    assert calc(inputs) == expected


################################################################################
# Password Generator


@pytest.mark.parametrize(
    "pool, size, pw",
    [
        ("abcdef", 8, "ddaceddc"),
        ("!@#$%", 8, "$$!#%$$#"),
        (string.ascii_lowercase, 20, "mynbiqpmzjplsgqejeyd"),
    ],
)
def test_simple_generator(pool, size, pw):
    random.seed(0)
    create_password = create_password_generator(pool)
    output = create_password(size)
    assert len(output) == size
    assert output == pw


@pytest.mark.parametrize(
    "min_uppercase, min_lowercase, min_punctuation, min_digits, pw, passes_test",
    [
        (1, 4, 1, 1, "Ufeda!123", True),
        (2, 4, 4, 3, "thisisnotgoingtopass", False),
    ],
)
def test_simple_checker(
    min_uppercase, min_lowercase, min_punctuation, min_digits, pw, passes_test
):
    password_checker = create_password_checker(
        min_uppercase, min_lowercase, min_punctuation, min_digits
    )
    result = password_checker(pw)
    assert result == passes_test
