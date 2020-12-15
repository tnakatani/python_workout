import pytest
from src.strings.ubbi_dubbi import ubbi_dubbi


@pytest.mark.parametrize(
    "inputs, expected_sum",
    [
        ("hello mother", "hubellubo mubothuber"),
        ("soap", "suboubap"),
    ],
)
def test_ubbi_dubbi(inputs, expected_sum):
    assert ubbi_dubbi(inputs) == expected_sum
