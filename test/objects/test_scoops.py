import mock
import pytest

from src.objects.scoops import (
    BigBowl,
    BowlWithLimitedScoops,
    Bread,
    LogFile,
    MaxScoopExceeded,
    Person,
    Phone,
    Scoop,
    SmartPhone,
    Transaction,
    WheatBread,
    WidthTooLargeError,
    create_scoops,
    Beverage,
    Bowl,
    Book,
    Shelf,
    Envelope,
    BigEnvelope,
    InsufficientPostage,
    Iphone,
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


def test_too_many_scoops():
    s1 = Scoop("chocolate")

    b = BowlWithLimitedScoops()
    with pytest.raises(MaxScoopExceeded):
        b.add_scoops(s1, s1, s1, s1)


def test_population():
    p1 = Person()
    p2 = Person()
    p3 = Person()
    p4 = Person()
    p5 = Person()
    assert Person.population == 5


def test_population_deletion():
    p1 = Person()
    p2 = Person()
    p3 = Person()
    p4 = Person()
    p5 = Person()
    for p in [p1, p2, p3, p4, p5]:
        p.__del__()
    assert Person.population == 0


def test_transactions():
    t1 = Transaction(25)
    t2 = Transaction(5)
    t3 = Transaction(-10)
    assert Transaction.balance == 20


def test_too_many_scoops_bigbowl():
    s1 = Scoop("chocolate")
    b = BigBowl()
    with pytest.raises(MaxScoopExceeded):
        b.add_scoops(s1, s1, s1, s1, s1, s1)


def test_envelope_with_insufficient_postage():
    e1 = Envelope(weight=200, postage=0)
    with pytest.raises(InsufficientPostage):
        e1.send()
    assert e1.was_sent == False


def test_envelope_with_sufficient_postage():
    e1 = Envelope(weight=200, postage=4000)
    e1.send()
    assert e1.was_sent == True


def test_bigenvelope_with_insufficient_postage():
    e1 = BigEnvelope(weight=200, postage=0)
    with pytest.raises(InsufficientPostage):
        e1.send()
    assert e1.was_sent == False


def test_bigenvelope_with_sufficient_postage():
    e1 = BigEnvelope(weight=200, postage=5000)
    e1.send()
    assert e1.postage_needed() == 3000
    assert e1.was_sent == True


def test_phone():
    p1 = Phone("1234567890")
    assert p1.format_phone_number() == "123-456-7890"


def test_smartphone():
    p1 = SmartPhone("1234567890")
    p1.run_app()
    assert p1.app_on == True


def test_iphone():
    p1 = Iphone("1113339876")
    assert p1.dial() == "one-one-one-three-three-three-nine-eight-seven-six"


def test_bread_with_two_slices():
    b1 = Bread()
    assert b1.get_nutrition(2) == {
        "calories": 134,
        "carbohydrates": 26,
        "fat": 2.2,
        "sodium": 0.288,
        "sugar": 2.8,
    }


def test_wheat_bread_with_three_slices():
    b1 = WheatBread()
    assert b1.get_nutrition(3) == {
        "calories": 240,
        "carbohydrates": 60,
        "fat": 0,
        "sodium": 0.51,
        "sugar": 12,
    }
