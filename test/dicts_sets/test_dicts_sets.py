import pytest

from src.dicts_sets.dicts_sets import *
from collections import Counter, defaultdict
from io import StringIO


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
