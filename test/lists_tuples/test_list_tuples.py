import pytest
from src.lists_tuples.list_tuples import *


@pytest.mark.parametrize('inputs, expected', [
    ('abc', 'ac'),
    ([1, 2, 3, 4], [1, 4]),
    ([[1, 2], [3, 4], [5, 6], [7, 8]], [[1, 2], [7, 8]])
])
def test_firstlast(inputs, expected):
    assert firstlast(inputs) == expected


@pytest.mark.parametrize('inputs, expected', [
    ([10, 20, 30, 40, 50, 60], [90, 120])
])
def test_even_odd_sums(inputs, expected):
    assert even_odd_sums(inputs) == expected


@pytest.mark.parametrize('inputs, expected', [
    ([10, 20, 30, 40, 50, 60], 50)
])
def test_plus_minus(inputs, expected):
    assert plus_minus(inputs) == expected


@pytest.mark.parametrize('inputs, expected', [
    ((), ()),
    ((10, 20, 30), 60),
    (('a', 'b', 'c'), 'abc'),
    (('abc', 'def'), 'abcdef'),
    ([10, 20, 30], 60)
])
def test_mysum(inputs, expected):
    assert mysum(*inputs) == expected


@pytest.mark.parametrize('inputs, expected', [
    ((10, 20, 'a', '30', 'bcd'), 60)
])
def test_sum_numeric(inputs, expected):
    assert sum_numeric(*inputs) == expected
