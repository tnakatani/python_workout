import pytest
import mock
from src.dicts_sets.dicts_sets import *
from collections import Counter, defaultdict
from io import StringIO


######################################################################
# Menu Items Exercise

def test_order_nothing(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO("done"))
    restaurant(MENU)
    captured_out, captured_err = capsys.readouterr()
    assert captured_out.endswith('Your total is 0\n')


def test_order_one_item(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO("sandwich" + "\n" +
                                              "done" + "\n"))
    restaurant(MENU)
    captured_out, captured_err = capsys.readouterr()
    assert f"sandwich costs 9.99, total is 9.99" in captured_out
    assert captured_out.endswith(f"Your total is 9.99\n")


def test_order_two_items(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO("sandwich" + "\n" +
                                              "coffee" + "\n" +
                                              "done\n"))
    restaurant(MENU)
    captured_out, captured_err = capsys.readouterr()
    assert f"sandwich costs 9.99, total is 9.99" in captured_out
    assert f"coffee costs 1.99, total is 11.98" in captured_out
    assert captured_out.endswith(f"Your total is 11.98\n")


def test_order_many_items(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO("sandwich" + "\n" +
                                              "coffee" + "\n" +
                                              "fries" + "\n" +
                                              "pancakes" + "\n" +
                                              "done\n"))
    restaurant(MENU)
    captured_out, captured_err = capsys.readouterr()
    assert f"sandwich costs 9.99, total is 9.99" in captured_out
    assert f"coffee costs 1.99, total is 11.98" in captured_out
    assert f"fries costs 2.99, total is 14.97" in captured_out
    assert f"pancakes costs 6.99, total is 21.96" in captured_out
    assert captured_out.endswith(f"Your total is 21.96\n")


def test_order_item_not_on_menu(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO("steak" + "\n" +
                                              "done\n"))
    restaurant(MENU)
    captured_out, captured_err = capsys.readouterr()
    assert f"Sorry, we are fresh out of steak" in captured_out
    assert captured_out.endswith(f"Your total is 0\n")


######################################################################
# Date Temperature Exercise

def test_no_date(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO("\n" +
                                              "done\n"))
    get_temp_by_date(TEMPS)
    captured_out, captured_err = capsys.readouterr()
    assert f"No query registered, try again" in captured_out


def test_one_date(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO("11/30/2020" + "\n" +
                                              "done\n"))
    get_temp_by_date(TEMPS)
    captured_out, captured_err = capsys.readouterr()
    assert f"11/29/2020 temperature: 40" in captured_out
    assert f"11/30/2020 temperature: 49" in captured_out
    assert f"12/01/2020 temperature: 40" in captured_out


def test_out_of_date(monkeypatch, capsys):
    monkeypatch.setattr('sys.stdin', StringIO("11/29/2020" + "\n" +
                                              "done\n"))
    get_temp_by_date(TEMPS)
    captured_out, captured_err = capsys.readouterr()
    assert f"Date range is out of bounds, try again." in captured_out


######################################################################
# Rainfall Exercise


def test_no_city(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("\n\n"))
    rainfall_report()
    captured_out, captured_err = capsys.readouterr()
    assert "No data registered." in captured_out


def test_missing_rainfall(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("Boston\n" +
                                              "\n\n"))
    rainfall_report()
    captured_out, captured_err = capsys.readouterr()
    assert "Not a valid value, try again." in captured_out


def test_invalid_rainfall(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("Boston\n" +
                                              "\n" +
                                              "foobar\n" +
                                              "\n\n"))
    rainfall_report()
    captured_out, captured_err = capsys.readouterr()
    assert "Not a valid value, try again." in captured_out


def test_one_city(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("Boston\n" +
                                              "12\n" +
                                              "\n\n"))
    rainfall_report()
    captured_out, captured_err = capsys.readouterr()
    assert f"Boston: 12mm" in captured_out


def test_multiple_city(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("Boston\n" +
                                              "12\n" +
                                              "Seattle\n" +
                                              "15\n" +
                                              "Louisville\n" +
                                              "7" +
                                              "\n\n"))
    rainfall_report()
    captured_out, captured_err = capsys.readouterr()
    assert f"Boston: 12mm" in captured_out
    assert f"Seattle: 15mm" in captured_out
    assert f"Louisville: 7mm" in captured_out


def test_update_city(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("Boston\n" +
                                              "12\n" +
                                              "Boston\n" +
                                              "20\n" +
                                              "\n\n"))
    rainfall_report()
    captured_out, captured_err = capsys.readouterr()
    assert f"Boston: 32mm" in captured_out


######################################################################
# Word Length Counter


"""
Note: Had trouble figuring out whether mock.patch needed "__builtins__.open"
or "builtins.open" or "main.open".  Still don't quite understand the nuance
between all of them.  One important note is that the 'file_path' passed to the
function doesn't really matter, you can pass it "file_path", "foobar", etc.

Ref (led me to answer): https://stackoverflow.com/a/33184416/12207563
Python doc: https://docs.python.org/3.6/library/unittest.mock.html#patch
"""


def test_word_length_freq_table():
    mock_open = mock.mock_open(read_data='a ab abc abcd')
    with mock.patch("builtins.open", mock_open) as m:
        result = word_length_freq_table('file_path')
    assert result == {1: 1, 2: 1, 3: 1, 4: 1}


################################################################################
# Dict Diff

"""
Note to self: pytest fixtures need to passed to a test function
in order to get the return value.
"""


@pytest.fixture
def simple_dict1():
    return {'a': 1, 'b': 2, 'c': 3}


@pytest.fixture
def simple_dict2():
    return {'a': 1, 'b': 2, 'c': 4}


@pytest.fixture
def simple_dict3():
    return {'a': 1, 'b': 2, 'd': 3}


def test_empty():
    assert dictdiff({}, {}) == {}


def test_same(simple_dict1):
    assert dictdiff(simple_dict1, simple_dict1) == {}


def test_simple_diff1(simple_dict1, simple_dict2):
    assert dictdiff(simple_dict1, simple_dict2) == {'c': [3, 4]}


def test_simple_diff2(simple_dict1, simple_dict3):
    assert dictdiff(simple_dict1, simple_dict3) == {
        'c': [3, None], 'd': [None, 3]}


def test_simple_diff_bw(simple_dict1, simple_dict3):
    assert dictdiff(simple_dict3, simple_dict1) == {
        'c': [None, 3], 'd': [3, None]}


################################################################################
# Dict Merge


def test_empty():
    assert dictmerge() == {}


def test_multi_dicts(simple_dict1, simple_dict2, simple_dict3):
    assert dictmerge(simple_dict1, simple_dict2, simple_dict3) == {
        'a': 1, 'b': 2, 'c': 4, 'd': 3
    }


################################################################################
# Dict Partition

def test_dictpartition(simple_dict1):
    assert dictpartition(simple_dict1, is_even) == ({'b': 2}, {'a': 1, 'c': 3})


################################################################################
# Different Numbers

@pytest.fixture
def empty_list():
    return []


@pytest.fixture
def list_of_integers():
    return [1, 2, 3, 1, 2, 3, 4, 1]


def test_empty(empty_list):
    assert get_unique_integers(empty_list) == 0


def test_get_unique_integers(list_of_integers):
    assert get_unique_integers(list_of_integers) == 4
