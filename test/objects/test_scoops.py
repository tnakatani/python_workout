from io import StringIO

import mock
import pytest

from src.objects.scoops import (
    LogFile,
    Scoop,
    WidthTooLargeError,
    create_scoops,
    Beverage,
    Bowl,
    Book,
    Shelf,
)


def test_scoops():
    scoop = Scoop("Chocolate")
    assert scoop.flavor == "Chocolate"


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (
            ("Chocolate", "Vanilla", "Strawberry"),
            ["Chocolate", "Vanilla", "Strawberry"],
        ),
        (
            ["Chocolate", "Vanilla", "Strawberry"],
            ["Chocolate", "Vanilla", "Strawberry"],
        ),
        (
            {"Chocolate", "Vanilla", "Strawberry"},
            ["Chocolate", "Vanilla", "Strawberry"],
        ),
    ],
)
def test_create_scoops_with_different_iterables(inputs, expected):
    assert all([flavor in expected for flavor in create_scoops(inputs)])


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (["milk", 60], ["milk", 60]),
        (["tea", 185], ["tea", 185]),
        (["beer", 45], ["beer", 45]),
    ],
)
def test_beverage(inputs, expected):
    bev = Beverage(inputs[0], inputs[1])
    assert bev.name == expected[0] and bev.temp == expected[1]


def test_beverage_default_temp():
    bev = Beverage("foobarbaz")
    assert bev.name == "foobarbaz" and bev.temp == 75


def test_logfile():
    open_mock = mock.mock_open()
    with mock.patch("builtins.open", open_mock, create=True):
        lf = LogFile("dummy.log")
        lf.write("foobarbaz")
    open_mock.assert_called_with("dummy.log", "w")
    open_mock.return_value.write.assert_called_once_with("foobarbaz")


def test_bowl():
    s1 = Scoop("chocolate")
    s2 = Scoop("vanilla")
    s3 = Scoop("persimmon")

    b = Bowl()
    b.add_scoops(s1, s2)
    b.add_scoops(s3)

    assert len(b.scoops) == 3
    assert s1 in b.scoops
    assert s2 in b.scoops
    assert s3 in b.scoops

    assert str(b) == "chocolate\nvanilla\npersimmon"


def test_books_price():
    b1 = Book(author="Foo Bar", title="Story of Foo", price=12.99, width=2)
    b2 = Book(author="Bar Baz", title="Story of Bar", price=10.99, width=1)
    b3 = Book(author="Baz Boz", title="Story of Baz", price=13.99, width=3)
    s = Shelf()
    s.add_books(b1, b2)
    s.add_books(b3)
    assert s.total_price() == (12.99 + 10.99 + 13.99)


def test_shelf_has_title():
    b1 = Book(author="Foo Bar", title="Story of Foo", price=12.99, width=2)
    s = Shelf()
    s.add_books(b1)
    assert s.has_book("Story of Foo") == True
    assert s.has_book("story of foo") == True
    assert s.has_book("Story of FooBarBaz") == False


def test_books_too_wide_for_shelf():
    b1 = Book(author="Foo Bar", title="Story of Foo", price=12.99, width=2)
    b2 = Book(author="Bar Baz", title="Story of Bar", price=10.99, width=1)
    b3 = Book(author="Baz Boz", title="Story of Baz", price=13.99, width=3)
    s = Shelf(width=1)
    with pytest.raises(WidthTooLargeError):
        s.add_books(b3)
