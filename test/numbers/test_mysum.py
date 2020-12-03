import pytest
from src.numbers.numbers import *


@pytest.mark.parametrize('inputs, expected_sum', [
    ((), 0),
    ((10,), 10),
    ((10, 20, 30), 60),
    ((10.5, 20, 30), 60.5)
])
def test_mysum(inputs, expected_sum):
    assert mysum(*inputs) == expected_sum
