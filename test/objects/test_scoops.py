from io import StringIO

import mock
import pytest

from src.objects.scoops import LogFile, Scoop, create_scoops, Beverage


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
    bev = Beverage('foobarbaz')
    assert bev.name == 'foobarbaz' and bev.temp == 75



def test_logfile():
    open_mock = mock.mock_open()
    with mock.patch("builtins.open", open_mock, create=True):
        lf = LogFile('dummy.log')
        lf.write('foobarbaz')
    open_mock.assert_called_with("dummy.log", "w")
    open_mock.return_value.write.assert_called_once_with("foobarbaz")


