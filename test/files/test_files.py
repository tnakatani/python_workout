import pytest
import mock
from io import StringIO
from src.files.files import *


################################################################################
# Final Line


def test_empty():
    mock_open = mock.mock_open(read_data='')
    with mock.patch("builtins.open", mock_open) as m:
        result = final_line('file_path')
    assert result == ''


def test_final_line():
    mock_open = mock.mock_open(read_data='a\nab\nabc\nabcd')
    with mock.patch("builtins.open", mock_open) as m:
        result = final_line('file_path')
    assert result == 'abcd'


################################################################################
# Sum Multi Column


def test_multi_columns_multi_rows():
    fake_tsv = StringIO('1\n'
                        '1\t2\n'
                        '1\t2\t3\n'
                        '1\t2\t3\t4')
    with mock.patch("builtins.open", return_value=fake_tsv):
        assert sum_multi_columns('file_path') == 32


################################################################################
# passwd_to_dict

def test_passwd_to_dict():
    fake_passwd = StringIO(
        '###############\n'
        '# User Database\n'
        '###############\n'
        '               \n'
        'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false\n'
        'root:*:0:0:System Administrator:/var/root:/bin/sh\n'
        'daemon:*:1:1:System Services:/var/root:/usr/bin/false\n')
    with mock.patch("builtins.open", return_value=fake_passwd):
        assert passwd_to_dict('file_path') == {'nobody': '-2', 'root': '0',
                                               'daemon': '1'}
