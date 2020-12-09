import csv, json
import os, glob
from functools import reduce
from typing import Dict, Set, List, Union, Callable, Tuple


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

def passwd_to_dict(file_path: str) -> Dict[any, any]:
    """Returns a dict based on /etc/passwd in which the dict’s keys are
    usernames and the values are the users’ IDs. Ignores comments and empty
    lines.

    Example:
        nobody:*:-2:-2::0:0:Unprivileged User:/var/empty:/usr/bin/false

    The first field (index 0) is the username (e.g. nobody), and the third
    field (index 2) is the user’s unique ID number (e.g. -2.
    """
    with open(file_path, 'r') as f:
        users = {}
        for line in f:
            if line.startswith('#') or line.strip() == '':
                continue
            fields = line.strip().split(':')
            user, id = fields[0], fields[2]
            users[user] = id
        return users