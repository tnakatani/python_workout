import mock
import pytest
from src.iterators_generators.iterators_generators import (
    Circle,
    CircleInherit,
    Circle_2,
    MyEnumerate,
    MyRange,
    circle,
    my_generator,
)

####################################################################################################
# e47: MyEnumerate


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (
            ["Chocolate", "Vanilla", "Strawberry"],
            [(0, "Chocolate"), (1, "Vanilla"), (2, "Strawberry")],
        ),
        (
            [1, 2, 3],
            [(0, 1), (1, 2), (2, 3)],
        ),
    ],
)
def test_myenumerate(inputs, expected):
    e = MyEnumerate(inputs)
    e_indexed = [(i, v) for i, v in e]
    assert e_indexed == expected


def test_myenumerate_enumerating_twice():
    e = MyEnumerate("abc")
    e_indexed = [(i, v) for i, v in e]
    f_indexed = [(i, v) for i, v in e]
    assert e_indexed == [(0, "a"), (1, "b"), (2, "c")]
    assert f_indexed == [(0, "a"), (1, "b"), (2, "c")]


def test_myenumerate_is_iterable():
    e = MyEnumerate("abc")
    assert hasattr(e, "__iter__")


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (
            ["Chocolate", "Vanilla", "Strawberry"],
            [(0, "Chocolate"), (1, "Vanilla"), (2, "Strawberry")],
        ),
        (
            [1, 2, 3],
            [(0, 1), (1, 2), (2, 3)],
        ),
    ],
)
def test_mygenerator(inputs, expected):
    g = my_generator(inputs)
    assert [(i, v) for i, v in g] == expected


####################################################################################################
# e48: Circle


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (
            ["a", "b", "c"],
            ["a", "b", "c", "a", "b", "c"],
        ),
        (
            [1, 2],
            [1, 2, 1, 2, 1, 2],
        ),
    ],
)
def test_circle(inputs, expected):
    c = Circle(inputs, 6)
    assert [i for i in c] == expected


def test_circle_inherit():
    c = CircleInherit("abc", 6)
    assert [i for i in c] == ["a", "b", "c", "a", "b", "c"]


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (
            ["a", "b", "c"],
            ["a", "b", "c", "a", "b", "c"],
        ),
        (
            [1, 2],
            [1, 2, 1, 2, 1, 2],
        ),
    ],
)
def test_circle_generator(inputs, expected):
    c = circle(inputs, 6)
    assert [i for i in c] == expected


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (
            [0, 10, 2],
            [0, 2, 4, 6, 8],
        ),
        (
            [0, 20, 10],
            [0, 10],
        ),
    ],
)
def test_myrange(inputs, expected):
    r = MyRange(inputs[0], inputs[1], inputs[2])
    assert [i for i in r] == expected
