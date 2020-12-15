import pytest
from src.strings.pig_latin import pig_latin


@pytest.mark.parametrize(
    "inputs, expected",
    [
        ("Oatmeal Apple Internet", "oatmealway appleway internetway"),
        ("Banana Bagel Happy Pig", "ananabay agelbay appyhay igpay"),
        ("This is a test translation", "histay isway away esttay ranslationtay"),
    ],
)
def test_pig_latin(inputs, expected):
    assert pig_latin(inputs) == expected
