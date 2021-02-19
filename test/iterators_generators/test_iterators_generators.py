import os

import mock
import pytest

from src.iterators_generators.iterators_generators import (
    Circle,
    CircleInherit,
    Circle_2,
    MyEnumerate,
    MyRange,
    all_lines,
    circle,
    my_generator, parallel_lines,
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


def test_myrange_with_defaults():
    r = MyRange(0, 5)
    s = MyRange(10)
    t = MyRange(0)
    assert [i for i in r] == [0, 1, 2, 3, 4]
    assert [i for i in s] == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert [i for i in t] == []


####################################################################################################
# e48: All of the files


@pytest.fixture
def test_dir(tmp_path):
    f = tmp_path / "f1.txt"
    g = tmp_path / "f2.txt"
    h = tmp_path / "f3.txt"
    i = tmp_path / "f4.txt"

    f.write_text("\n".join(["foo", "bar", "baz"]))
    g.write_text("\n".join(["one", "two", "three"]))
    h.write_text(
        """This is the first line of a big file
and this is the second line
and this is, to no one's surprise, the third line
but the biggest word will probably be encyclopedia"""
    )
    i.write_text("")
    return tmp_path


def test_all_lines(test_dir):
    assert len([i for i in all_lines(test_dir)]) == 10


@pytest.fixture
def test_empty_dir(tmp_path):
    return tmp_path


def test_all_lines_empty_dir(test_empty_dir):
    assert len([i for i in all_lines(test_empty_dir)]) == 0


def test_parallel_lines(test_dir):
    result = [i for i in parallel_lines(test_dir) if i]
    print(result)
    assert len(result) == 10


def test_parallel_lines_with_filter(test_dir):
    result = [i for i in parallel_lines(test_dir, 'foo') if i]
    print(result)
    assert len(result) == 1
