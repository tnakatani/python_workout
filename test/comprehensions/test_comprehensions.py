from unittest import mock

from io import StringIO

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
Professor Zöllner of Leipsic was an ardent exponent of the theory in the 'seventies' and some authors hold that even the ancient writings of the East contain attempts to express Four-Dimensional concepts.
"""
    )
    return f


def test_filter_to_lexically_diverse(book_sample):
    assert filter_to_lexically_diverse(book_sample) == [
        """Professor Zöllner of Leipsic was an ardent exponent of the theory in the 'seventies' and some authors hold that even the ancient writings of the East contain attempts to express Four-Dimensional concepts."""
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
        (lambda x: x * x, {"a": 1, "b": -2, "c": 3}, {"a": 1, "b": 4, "c": 9}),
    ],
)
def test_transform_values(f, d, output):
    assert transform_values(f, d) == output


def test_get_filename_and_size(fs):
    fs.create_file("/home/alpha.txt", st_size=128)
    fs.create_file("/home/beta.txt", st_size=512)
    fs.create_file("/home/gamma.txt", st_size=256)
    assert get_filename_and_size("/home/") == {
        "alpha.txt": 128,
        "beta.txt": 512,
        "gamma.txt": 256,
    }


################################################################################
# Supervocalic


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (
            "The ambidextrous clown wowed the businesswoman",
            ("ambidextrous", "businesswoman"),
        ),
        (
            "The delusional revolutionary found zen beneath a sequoia tree",
            ("delusional", "revolutionary", "sequoia"),
        ),
    ],
)
def test_get_supervocalic(inputs, expected):
    assert get_supervocalic(inputs) == expected


@pytest.mark.parametrize(
    "inputs, keywords, expected",
    [
        ("The ambidextrous clown wowed the businesswoman", ["clown", "wowed"], True),
        (
            "The delusional revolutionary found zen beneath a sequoia tree",
            ("zen", "fern"),
            False,
        ),
    ],
)
def test_contain_keywords(inputs, keywords, expected):
    assert contain_keywords(inputs, keywords) == expected


def test_passwd_to_dict():
    fake_passwd = StringIO(
        "###############\n"
        "# User Database\n"
        "###############\n"
        "               \n"
        "nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false\n"
        "root:*:0:0:System Administrator:/var/root:/bin/sh\n"
        "daemon:*:1:1:System Services:/var/root:/usr/bin/false\n"
        "foobarbaz:incomplete_data:info\n"
    )
    with mock.patch("builtins.open", return_value=fake_passwd):
        assert get_passwd_shells("file_path") == {"info", "/usr/bin/false", "/bin/sh"}


def test_passwd_to_dict():
    fake_passage = StringIO(
        """The highest points on any variant of the trail are the Col des Fours in France and the Fenêtre
d'Arpette in Switzerland, both at an altitude of 2,665 m (8,743 ft). This is not high enough 
to cause altitude sickness for most people, nevertheless the trail provides a tough physical
challenge. Experience of walking in mountain country is vital and, because mountain weather
can change very rapidly, participants on the Tour du Mont Blanc should be suitably equipped."""
    )
    with mock.patch("builtins.open", return_value=fake_passage):
        assert get_word_lengths("file_path") == {
            1: {"m", "a"},
            2: {"in", "at", "on", "to", "is", "du", "be", "an", "of"},
            3: {"for", "des", "col", "the", "not", "can", "any", "and", "are"},
            4: {"and", "both", "ft", "high", "mont", "most", "this", "tour", "very"},
            5: {"fours", "trail", "2665", "cause", "tough", "vital", "blanc"},
            6: {"should", "8743", "change", "enough", "points", "france"},
            7: {
                "because",
                "country",
                "fenêtre",
                "highest",
                "people",
                "variant",
                "walking",
                "weather",
            },
            8: {
                "altitude",
                "mountain",
                "physical",
                "provides",
                "rapidly",
                "sickness",
                "suitably",
            },
            9: {"equipped", "d'arpette"},
            10: {"challenge", "experience"},
            12: {"participants", "switzerland", "nevertheless"},
        }


################################################################################
# Genatria


def test_make_genatria():
    assert make_genatria() == {
        "a": 1,
        "b": 2,
        "c": 3,
        "d": 4,
        "e": 5,
        "f": 6,
        "g": 7,
        "h": 8,
        "i": 9,
        "j": 10,
        "k": 11,
        "l": 12,
        "m": 13,
        "n": 14,
        "o": 15,
        "p": 16,
        "q": 17,
        "r": 18,
        "s": 19,
        "t": 20,
        "u": 21,
        "v": 22,
        "w": 23,
        "x": 24,
        "y": 25,
        "z": 26,
    }


def test_config_to_dict():
    fake_config = StringIO("a=1\n"
                           "b=2\n" 
                           "c=/etc/passwd")
    with mock.patch("builtins.open", return_value=fake_config):
        assert config_to_dict("file_path") == {"a": 1, "b": 2, "c": "/etc/passwd"}
