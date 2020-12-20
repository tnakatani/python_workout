import pytest

from src.comprehensions.comprehensions import *


################################################################################
# Join Numbers


def test_join_numbers():
    assert join_numbers(range(3)) == "1, 2, 3"


def test_join_numbers_below_ten():
    assert join_numbers_below_ten(range(20)) == "1, 2, 3, 4, 5, 6, 7, 8, 9"


@pytest.fixture
def text_file(tmp_path):
    f = tmp_path / "text_file.txt"
    f.write_text(
        """foo bar baz
baz bar foo
foo foo foo"""
    )
    return f


def test_reverse_lines_in_file(text_file):
    assert reverse_lines_in_file(text_file) == [
        "zab rab oof",
        "oof rab zab",
        "oof oof oof",
    ]


################################################################################
# Sum Numbers


@pytest.mark.parametrize(
    "inputs, expected", [((""), 0), (("               "), 0), (("!!@@!!@@@@@!!@@"), 0)]
)
def test_no_numbers(inputs, expected):
    assert sum_numbers(inputs) == expected


@pytest.mark.parametrize(
    "inputs, expected", [(("10 20 a 30 bcd 40"), 100), (("3 *** 9 @foo 10"), 22)]
)
def test_sum_numbers(inputs, expected):
    assert sum_numbers(inputs) == expected


@pytest.fixture
def book_sample(tmp_path):
    f = tmp_path / "text_file.txt"
    f.write_text(
        """THE MEANING OF FOUR-DIMENSIONAL SPACE.
The main line of thought developed in these pages has no claims to originality. 
Professor Zöllner of Leipsic was an ardent exponent of the theory in the 'seventies' and some 
authors hold that even the ancient writings of the East contain attempts to express 
Four-Dimensional concepts.
"""
    )
    return f


def test_filter_to_lexically_diverse(book_sample):
    assert filter_to_lexically_diverse(book_sample) == [
        "Professor Zöllner of Leipsic was an ardent exponent of the theory in the 'seventies' and "
        "some authors hold that even the ancient writings of the East contain attempts to express "
        "Four-Dimensional concepts."
    ]


@pytest.mark.parametrize(
    "inputs, expected",
    [
        ("123-456-7890", "124-456-7890"),
        ("123-333-4444", "124-333-4444"),
        ("123-777-8888", "123-777-8888"),
    ],
)
def test_change_area_code(inputs, expected):
    assert change_area_code(inputs) == expected


################################################################################
# Flatten


@pytest.mark.parametrize(
    "inputs, expected",
    [
        ([[], []], []),
        ([[1, 2], [3, 4]], [1, 2, 3, 4]),
        ([["abc", "def"], ["ghi", "jkl"]], ["abc", "def", "ghi", "jkl"]),
    ],
)
def test_flatten(inputs, expected):
    assert flatten(inputs) == expected


@pytest.mark.parametrize(
    "inputs, expected",
    [
        ([[], []], []),
        ([[1, 2], [3, 4]], [1, 3]),
        ([[12, 14], [2, 8]], []),
        ([["one-hundred", "fourteen"], ["2", "3"]], [3]),
    ],
)
def test_flatten_odd_ints(inputs, expected):
    assert flatten_odd_ints(inputs) == expected


def test_get_children():
    tree = {
        "foo": ["foo", "far", "faz"],
        "bar": ["boo", "bar", "baz"],
        "zab": ["zoo", "zar", "zaz"],
    }
    assert get_children(tree) == [
        "foo",
        "far",
        "faz",
        "boo",
        "bar",
        "baz",
        "zoo",
        "zar",
        "zaz",
    ]


def test_sort_children_by_oldest():
    tree = {
        "foo": [
            {"name": "foo", "age": 12},
            {"name": "far", "age": 14},
            {"name": "faz", "age": 16},
        ],
        "bar": [
            {"name": "boo", "age": 22},
            {"name": "bar", "age": 34},
            {"name": "baz", "age": 46},
        ],
        "zab": [
            {"name": "zoo", "age": 2},
            {"name": "zar", "age": 4},
            {"name": "zaz", "age": 6},
        ],
    }
    assert sort_children_by_oldest(tree) == [
        "baz",
        "bar",
        "boo",
        "faz",
        "far",
        "foo",
        "zaz",
        "zar",
        "zoo",
    ]


@pytest.fixture
def simple_file(tmp_path):
    f = tmp_path / "filename.txt"
    f.write_text(f"this is a test\nof my translation program\n")
    return f


def test_simple(simple_file):
    assert (
        plfile(simple_file)
    ) == "histay isway away esttay ofway ymay ranslationtay rogrampay"


def test_funcfile(simple_file):
    assert (
        funcfile(simple_file, to_pig_latin)
        == "histay isway away esttay ofway ymay ranslationtay rogrampay"
    )
    assert (
        funcfile(simple_file, cap_every_odd_letter)
        == "ThIs Is A TeSt Of My TrAnSlAtIoN PrOgRaM"
    )


def test_dict_to_list_of_tuples():
    list_dicts = [
        {"foo": 1, "bar": 2, "baz": 3},
        {"bar": 2, "baz": 3, "zab": 5},
        {"baz": 3, "buz": 2, "zooz": 200},
    ]
    assert dict_to_list_of_tuples(list_dicts) == [
        ("foo", 1),
        ("bar", 2),
        ("baz", 3),
        ("bar", 2),
        ("baz", 3),
        ("zab", 5),
        ("baz", 3),
        ("buz", 2),
        ("zooz", 200),
    ]


def test_get_most_common_scores():
    list_dicts = [
        {"foo": [85, 88, 99], "bar": [33, 64, 88], "baz": [34, 64, 86]},
        {"bar": [83, 22, 78], "baz": [83, 64, 55], "zab": [11, 22, 33]},
        {"baz": [88, 98, 78], "buz": [99, 99, 99], "zooz": [83, 99, 34]},
    ]
    assert get_most_common_score(list_dicts) == [(99, 5), (88, 3), (64, 3)]


################################################################################
# Flip Dict


@pytest.mark.parametrize(
    "input, expected",
    [
        ({}, {}),
        ({"a": 1}, {1: "a"}),
        ({"a": 1, "b": 2, "c": 3}, {1: "a", 2: "b", 3: "c"}),
        ({"a": 1, "a": 2, "a": 3}, {3: "a"}),
    ],
)
def test_flipped_dict(input, expected):
    assert flip_dict(input) == expected


def test_get_vowel_count():
    assert get_vowel_count("iconic too so treasure") == {
        "so": 1,
        "too": 2,
        "iconic": 3,
        "treasure": 4,
    }


################################################################################
# Transform Values


@pytest.mark.parametrize(
    "f,d,output",
    [
        (abs, {"a": 1, "b": -2, "c": 3}, {"a": 1, "b": 2, "c": 3}),
        (len, {"first": "foo", "last": "barbaz"}, {"first": 3, "last": 6}),
        (lambda x: x*x, {"a": 1, "b": -2, "c": 3}, {"a": 1, "b": 4, "c": 9}),
    ],
)
def test_transform_values(f, d, output):
    assert transform_values(f, d) == output
