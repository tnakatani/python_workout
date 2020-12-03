import pytest
from src.strings.strsort import strsort


@pytest.mark.parametrize('inputs, expected', [
    ("cba", "abc"),
    ("Harold met Sascha", "Hadlor emt Saachs"),
])
def test_strsort(inputs, expected):
    assert strsort(inputs) == expected
