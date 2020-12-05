import pytest
from src.lists_tuples.list_tuples import *
from collections import namedtuple


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


PEOPLE_1 = [{'first': 'Reuven', 'last': 'Lerner',
           'email': 'reuven@lerner.co.il'},
          {'first': 'Donald', 'last': 'Trump',
           'email': 'president@whitehouse.gov'},
          {'first': 'Vladimir', 'last': 'Putin',
           'email': 'president@kremvax.ru'}
          ]


def test_alphabetize_names():
    assert PEOPLE_1[0]['last'] == 'Lerner'
    assert PEOPLE_1[1]['last'] == 'Trump'
    assert PEOPLE_1[2]['last'] == 'Putin'

    output = alphabetize_names(PEOPLE_1)
    assert output[0]['last'] == 'Lerner'
    assert output[1]['last'] == 'Putin'
    assert output[2]['last'] == 'Trump'


@pytest.mark.parametrize('inputs, expected', [
    (['foo', 'bzz', 'bar', 'booboo'], ['bzz', 'bar', 'foo', 'booboo'])
])
def test_count_vowels(inputs, expected):
    assert count_vowels(inputs) == expected
    assert count_vowels_v2(inputs) == expected


@pytest.mark.parametrize('inputs, expected', [
    ([[1, 2], [0, 1], [5, 4]], [1, 3, 9])
])
def test_sort_summed(inputs, expected):
    assert sort_summed(inputs) == expected


@pytest.mark.parametrize('inputs, expected', [
    (['this', 'is', 'an', 'elementary', 'test', 'example'], 'elementary')
])
def test_most_repeating_word(inputs, expected):
    assert most_repeating_word(inputs) == expected


PEOPLE_2 = [('Donald', 'Trump', 7.85),
          ('Vladimir', 'Putin', 3.626),
          ('Jinping', 'Xi', 10.603)]


def test_with_people():
    output = format_sort_records(PEOPLE_2)
    assert isinstance(output, list)
    assert all(isinstance(x, str) for x in output)

    assert output[0][:10].strip() == 'Putin'
    assert output[0][10:20].strip() == 'Vladimir'
    assert output[0][20:].strip() == '3.63'


Person = namedtuple('Person', ['first', 'last', 'distance'])


PEOPLE_3 = [Person('Donald', 'Trump', 7.85),
          Person('Vladimir', 'Putin', 3.626),
          Person('Jinping', 'Xi', 10.603)]

def test_with_people_v2():
    output = format_sort_records_v2(PEOPLE_3)
    assert isinstance(output, list)
    assert all(isinstance(x, str) for x in output)

    assert output[0][:10].strip() == 'Putin'
    assert output[0][10:20].strip() == 'Vladimir'
    assert output[0][20:].strip() == '3.63'
