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
# /etc/passwd to dict

def test_passwd_to_dict():
    fake_passwd = StringIO(
        '###############\n'
        '# User Database\n'
        '###############\n'
        '               \n'
        'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false\n'
        'root:*:0:0:System Administrator:/var/root:/bin/sh\n'
        'daemon:*:1:1:System Services:/var/root:/usr/bin/false\n'
        'foobarbaz:incomplete_data:info\n'
    )
    with mock.patch("builtins.open", return_value=fake_passwd):
        assert passwd_to_dict('file_path') == {
            'daemon': {'home_dir': '/var/root', 'id': '1',
                       'shell': '/usr/bin/false'},
            'nobody': {'home_dir': '/var/empty', 'id': '-2',
                       'shell': '/usr/bin/false'},
            'root': {'home_dir': '/var/root', 'id': '0', 'shell': '/bin/sh'}}


################################################################################
# Word Count

def test_word_count():
    text_file = StringIO(
       "foo bar baz\n" # 11 chars
       "foo bar 文書\n" # 10 chars
    )
    with mock.patch("builtins.open", return_value=text_file):
        result = word_count('file_path')
        assert result['line_count'] == 2
        assert result['word_count'] == 6
        assert result['words_uniq'] == 4
        assert result['char_count'] == 17

