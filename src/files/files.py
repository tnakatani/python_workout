import csv, json
import os, glob
from functools import reduce
from typing import Dict, Set, List, Union, Callable, Tuple
import logging


################################################################################
# Final Line

def final_line(file_path: str) -> str:
    """Takes a filename as an argument and returns that file’s final line"""
    with open(file_path) as f:
        last_line = ''
        for line in f:
            last_line = f.readline()
        return last_line


################################################################################
# Sum Multi Column


def is_empty_file(file_path: str) -> bool:
    """Checks whether a file is empty, i.e. has 0 bytes.
    Returns True is file is empty"""
    return os.stat(file_path).st_size == 0


def sum_multi_columns(file_path: str) -> int:
    """Reads a two-column TSV. Multiplies each first number by the second,
    and then sums the results from all the lines.  Ignores any line that
    doesn’t contain two or more numeric columns."""
    with open(file_path, 'r') as f:
        nums = []
        for line in f:
            split = line.rstrip().split('\t')
            if len(split) >= 2:
                line = [int(i) for i in split]
                nums.append(reduce(lambda x, y: x * y, line))
        return sum(nums)


################################################################################
# /etc/passwd to dict

def passwd_to_dict(file_path: str) -> Dict[any, Dict[str, str]]:
    """Returns a dict based on /etc/passwd in which the dict’s keys are
    usernames and the values are dicts with keys (and
    appropriate values) for user ID, home directory, and shell. Ignores
    comments and empty lines.

    Example:
        nobody:*:-2:-2::0:0:Unprivileged User:/var/empty:/usr/bin/false

    The first field (index 0) is the username (e.g. nobody), and the third
    field (index 2) is the user’s unique ID number (e.g. -2.
    """
    with open(file_path, 'r') as f:
        users = {}
        for line in f:
            try:
                fields = line.strip().split(':')
                user, id, home_dir, shell = fields[0], fields[2], \
                                            fields[5], fields[6]
            except IndexError as e:
                logging.warning(f"{fields} has unexpected format, skipping")
                continue
            users[user] = {'id': id, 'home_dir': home_dir, 'shell': shell}
        return users


################################################################################
# Word Count


def count_chars(word_list: List[str]) -> int:
    """Counts the number of characters from a string of tokens. Count
    doesn't include white space delimiters or newlines.

    Args:
        text (str): a string of tokens of an arbitrary length

    Returns:
        int: Number of characters
    """
    count = 0
    for char in word_list:
        count += len(char)
    return count


def normalize(text):
    """Do basic word token normalization such as lowercase, stripping
    newline, white space delimited tokenization.

    Args:
        text (str): a string of tokens of an arbitrary length

    Returns:
        tokens (List[str]): a list of normalized word tokens
    """
    return text.strip().lower().split(' ')


def word_count(file_path: str) -> Dict[str, int]:
    """Takes a filename as input measures the following:
    1. Number of characters (not including whitespace)
    2. Number of words (white space delimited)
    3. Number of lines
    4. Number of unique words (case insensitive)

    Args:
        file_path (str): Path to text file
    """
    with open(file_path, 'r') as f:
        counts = {'char_count': 0, 'word_count': 0, 'line_count': 0,
                  'words_uniq': 0, }
        all_words = set()
        for line in f:
            token_list = normalize(line)
            counts['char_count'] += count_chars(token_list)
            counts['word_count'] += len(token_list)
            counts['line_count'] += 1
            all_words.update(token_list)
        counts['words_uniq'] = len(all_words)
        return counts



