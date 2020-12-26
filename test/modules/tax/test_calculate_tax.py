from io import StringIO
from math import isclose
from src.modules.tax.freedonia import calc_price_with_tax
from src.modules.menu.menu import menu

import pytest

################################################################################
# calculate_tax


@pytest.mark.parametrize(
    "amount,state,hour,tax",
    [
        (500, "Harpo", 12, 625),
        (500, "Harpo", 21, 718),
    ],
)
def test_calculate_tax(amount, state, hour, tax):
    assert isclose(calc_price_with_tax(amount, state, hour), tax, rel_tol=0.05)


################################################################################
# menu.py


def funca_test():
    return "A"


def funcb_test():
    return "B"


@pytest.mark.parametrize(
    "choice, expected",
    [
        ("a", "A"),
        ("b", "B"),
    ],
)
def test_menu_with_valid_keys(monkeypatch, capsys, choice, expected):
    monkeypatch.setattr("sys.stdin", StringIO(f"{choice}\n"))
    result = menu(a=funca_test, b=funcb_test)
    captured_out, captured_err = capsys.readouterr()
    assert result == expected


@pytest.mark.parametrize(
    "first_choice, second_choice",
    [
        ("foobar", "a"),
        ("this is an invalid key", "b"),
    ],
)
def test_menu_with_invalid_keys(monkeypatch, capsys, first_choice, second_choice):
    """Test menu with an invalid choice, then close function with valid choice"""
    monkeypatch.setattr("sys.stdin", StringIO(f"{first_choice}\n{second_choice}\n"))
    result = menu(a=funca_test, b=funcb_test)
    captured_out, captured_err = capsys.readouterr()
    assert f"Function keyword '{first_choice}' does not exist" in captured_out
