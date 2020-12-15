from io import StringIO

import mock
import pytest

from src.files.files import *


################################################################################
# Final Line


def test_empty():
    mock_open = mock.mock_open(read_data="")
    with mock.patch("builtins.open", mock_open) as m:
        result = final_line("file_path")
    assert result == ""


def test_final_line():
    mock_open = mock.mock_open(read_data="a\nab\nabc\nabcd")
    with mock.patch("builtins.open", mock_open) as m:
        result = final_line("file_path")
    assert result == "abcd"


################################################################################
# Sum Multi Column


def test_multi_columns_multi_rows():
    fake_tsv = StringIO("1\n" "1\t2\n" "1\t2\t3\n" "1\t2\t3\t4")
    with mock.patch("builtins.open", return_value=fake_tsv):
        assert sum_multi_columns("file_path") == 32


################################################################################
# /etc/passwd to dict


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
        assert passwd_to_dict("file_path") == {
            "daemon": {"home_dir": "/var/root", "id": "1", "shell": "/usr/bin/false"},
            "nobody": {"home_dir": "/var/empty", "id": "-2", "shell": "/usr/bin/false"},
            "root": {"home_dir": "/var/root", "id": "0", "shell": "/bin/sh"},
        }


################################################################################
# Word Count


def test_word_count():
    text_file = StringIO("foo bar baz\n" "foo bar 文書\n")  # 11 chars  # 10 chars
    with mock.patch("builtins.open", return_value=text_file):
        result = word_count("file_path")
        assert result["line_count"] == 2
        assert result["word_count"] == 6
        assert result["words_uniq"] == 4
        assert result["char_count"] == 17


################################################################################
# Longest word per file/files


@pytest.fixture
def empty_file(tmp_path):
    f = tmp_path / "emptyfile.txt"
    f.write_text("")
    return f


@pytest.fixture
def small_file(tmp_path):
    f = tmp_path / "smallfile.txt"
    f.write_text(
        """This is the first line
and this is the second line"""
    )
    return f


@pytest.fixture
def big_file(tmp_path):
    f = tmp_path / "bigfile.txt"
    f.write_text(
        """This is the first line of a big file
and this is the second line
and this is, to no one's surprise, the third line
but the biggest word will probably be encyclopedia

here is a website: https://www.gutenberg.org
here are some garbled text: ??faa faa ;;;??
"""
    )
    return f


def test_small_file(small_file):
    assert find_longest_word(small_file) == "second"


def test_big_file(big_file):
    assert find_longest_word(big_file) == "encyclopedia"


def test_empty_directory(tmp_path):
    assert find_all_longest_words(tmp_path) == {}


def test_empty_file(tmp_path, empty_file):
    assert find_all_longest_words(tmp_path) == {"emptyfile.txt": ""}


def test_all_files(tmp_path, empty_file, small_file, big_file):
    assert find_all_longest_words(tmp_path) == {
        "emptyfile.txt": "",
        "smallfile.txt": "second",
        "bigfile.txt": "encyclopedia",
    }


################################################################################
# Reading / Writing CSV


@pytest.fixture
def passwd_file(tmp_path):
    f = tmp_path / "passwd"
    f.write_text(
        """
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
atara:x:1004:1005:Atara Lerner-Friedman,,,:/home/atara:/bin/bash
shikma:x:1005:1006:Shikma Lerner-Friedman,,,:/home/shikma:/bin/bash
# Here is a comment
amotz:x:1006:1007:Amotz Lerner-Friedman,,,:/home/amotz:/bin/bash
"""
    )
    return f


def test_empty_file(tmp_path, empty_file):
    passwd_to_tsv(empty_file, "output.tsv")
    csv_content = open("output.tsv").read()
    assert len(csv_content) == 0


def test_passwd_to_csv(passwd_file):
    passwd_to_tsv(passwd_file, "output.tsv")
    csv_content = open("output.tsv").read()
    assert len(csv_content) == 95
    assert csv_content.splitlines()[0] == "root\t0"
    assert csv_content.splitlines()[-1] == "amotz\t1006"


################################################################################
# JSON


@pytest.fixture
def score_file_1(tmp_path):
    j1 = tmp_path / "9a.json"
    j1.write_text(
        """
[{"math" : 90, "literature" : 98, "science" : 97},
 {"math" : 65, "literature" : 79, "science" : 85},
 {"math" : 78, "literature" : 83, "science" : 75},
 {"math" : 92, "literature" : 78, "science" : 85},
 {"math" : 100, "literature" : 80, "science" : 90}
]
"""
    )
    return j1


@pytest.fixture
def score_file_2(tmp_path):
    j2 = tmp_path / "9b.json"
    j2.write_text(
        """
[{"math" : 70, "literature" : 98, "science" : 97},
 {"math" : 65, "literature" : 83, "science" : 70},
 {"math" : 58, "literature" : 83, "science" : 75},
 {"math" : 72, "literature" : 78, "science" : 85},
 {"math" : 100, "literature" : 80, "science" : 90}
]
"""
    )
    return j2


def test_score_file(tmp_path, score_file_1, score_file_2):
    analyze_scores(tmp_path, "output.tsv")
    csv_content = open("output.tsv").read()
    assert csv_content.splitlines()[0].split("\t") == [
        "class",
        "subject",
        "min_score",
        "max_score",
        "avg_score",
    ]
    assert csv_content.splitlines()[1].split("\t")[0] == "9a"
    assert csv_content.splitlines()[6].split("\t")[0] == "9b"


################################################################################
# Reverse lines


@pytest.fixture
def big_file(tmp_path):
    f = tmp_path / "bigfile.txt"
    f.write_text(
        """This is the first line of a big file
and this is the second line
and this is, to no one's surprise, the third line
but the biggest word will probably be encyclopedia"""
    )
    return f


def test_reversing_lines(big_file):
    reverse_lines(big_file, "output.txt")
    content = open("output.txt").read()
    assert len(content) == 166
    assert content[:18] == "elif gib a fo enil"
    assert content[-18:] == "w tseggib eht tub\n"
