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
