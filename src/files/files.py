import csv
import json
import logging
import os
import pathlib
import re
from collections import defaultdict
from functools import reduce
from typing import Dict, List


################################################################################
# Final Line


def final_line(file_path: str) -> str:
    """Takes a filename as an argument and returns that file’s final line"""
    with open(file_path) as f:
        last_line = ""
        for _ in f:
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
    with open(file_path, "r") as f:
        nums = []
        for line in f:
            split = line.rstrip().split("\t")
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
    with open(file_path, "r") as f:
        users = {}
        for line in f:
            try:
                fields = line.strip().split(":")
                user, id, home_dir, shell = fields[0], fields[2], fields[5], fields[6]
            except IndexError:
                logging.warning(f"{fields} has unexpected format, skipping")
                continue
            users[user] = {"id": id, "home_dir": home_dir, "shell": shell}
        return users


################################################################################
# Word Count


def count_chars(word_list: List[str]) -> int:
    """Counts the number of characters from a string of tokens. Count
    doesn't include white space delimiters or newlines.

    Args:
        word_list (str): a string of tokens of an arbitrary length

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

    def _replace_urls(text):
        url_regex = (
            r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,"
            r"}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|("
            r"?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
        )
        text = re.sub(url_regex, "<URL>", text)
        return text

    def _simplify_punctuation(text):
        """
        This functions simplifies doubled or more complex punctuation. The exception is '...'.
        """
        corrected = str(text)
        corrected = re.sub(r"([!?,;])\1+", r"\1", corrected)
        corrected = re.sub(r"\.{2,}", r"...", corrected)
        return corrected

    text = text.strip().lower()
    text = _replace_urls(text)
    text = _simplify_punctuation(text)
    return text.split(" ")

    # for token in tokens:
    #     if "http" in token:
    #         continue
    #     norm.append(token)
    return no_url


def word_count(file_path: str) -> Dict[str, int]:
    """Takes a filename as input measures the following:
    1. Number of characters (not including whitespace)
    2. Number of words (white space delimited)
    3. Number of lines
    4. Number of unique words (case insensitive)

    Args:
        file_path (str): Path to text file
    """
    with open(file_path, "r") as f:
        counts = {
            "char_count": 0,
            "word_count": 0,
            "line_count": 0,
            "words_uniq": 0,
        }
        all_words = set()
        for line in f:
            token_list = normalize(line)
            counts["char_count"] += count_chars(token_list)
            counts["word_count"] += len(token_list)
            counts["line_count"] += 1
            all_words.update(token_list)
        counts["words_uniq"] = len(all_words)
        return counts


################################################################################
# Longest word per file/files


def find_longest_word(fp: str) -> str:
    """Takes a filename as an argument and returns the longest word found in the file

    Args:
        fp: File path

    Returns:
        Longest word found in the file
    """

    # Attempt 1
    # with open(fp, 'r') as f:
    #     longest = ''
    #     for line in f:
    #         tokens = set(normalize(line))
    #         words = {t:len(t) for t in tokens}
    #         max_word = max(words, key=words.get)
    #         if len(max_word) > len(longest):
    #             longest = max_word
    #     return longest

    # Attempt 2
    with open(fp, "r") as f:
        words = set()
        for line in f:
            words.update(set(normalize(line)))
        try:
            return max(words, key=len)
        except ValueError:
            return ""


def find_all_longest_words(fd: str) -> Dict[str, str]:
    """Takes a directory name and returns a dict in which the keys are filenames and the values
    are the longest words from each file.

    Args:
        fd: File directory

    Returns:
        Dict with filenames as keys, and longest words as value.
    """

    # Attempt 1:
    # file_paths = os.listdir(fd)
    # longest_words = {}
    # for fp in file_paths:
    #     longest_words[fp] = find_longest_word(os.path.join(fd, fp))

    # Attempt 2:
    file_paths = pathlib.Path(fd)
    longest_words = {
        fp.name: find_longest_word(fp)
        for fp in file_paths.iterdir()
        if file_paths.is_dir()
    }
    return longest_words


################################################################################
# Reading / Writing CSV


def read_passwd(read_path: str) -> List[List[str]]:
    """Read file and return a list of lists

    Args:
        read_path: Path to /etc/passwd file
    """
    # Attempt 1:
    # rows = []
    # with open(read_path, "r") as f:
    #     for line in f:
    #         try:
    #             fields = line.strip().split(":")
    #             user_and_id = [fields[0], fields[2]]
    #         except IndexError:
    #             logging.warning(f"{fields} has unexpected format, skipping")
    #             continue
    #         rows.append(user_and_id)
    # return rows

    # Attempt 2:
    rows = []
    with open(read_path, "r") as f:
        reader = csv.reader(f, delimiter=":")
        for line in reader:
            if len(line) <= 1:
                continue
            rows.append([line[0], line[2]])
    return rows


def write_passwd(user_list: List[List[str]], write_path: str) -> None:
    """Takes a list of lists and writes them to a TSV file

    Args:
        write_path: Path to output TSV file
    """
    with open(write_path, "w") as f:
        writer = csv.writer(f, delimiter="\t")
        for user in user_list:
            writer.writerow(user)


def passwd_to_tsv(read_path: str, write_path: str) -> None:
    """Reads the standard Unix /etc/passwd file and writes a TSV file containing the username
    and user ID. Ignores commented lines.

    Args:
        read_path: Path to /etc/passwd file
        write_path: Path to output TSV file
    """
    # Attempt 1:
    # rows = read_passwd(read_path)
    # write_passwd(rows, write_path)

    # Attempt 2:
    with open(read_path, "r") as rf, open(write_path, "w") as wf:
        reader = csv.reader(rf, delimiter=":")
        writer = csv.writer(wf, delimiter="\t")
        for line in reader:
            if len(line) > 1:
                writer.writerow([line[0], line[2]])


################################################################################
# JSON


def analyze_scores(read_path: str, write_path: str) -> None:
    """Reads a directory with multiple JSON files of test scores.  Calculates the highest, lowest,
    and average test scores for each subject in each class, and writes them to a TSV file"""
    file_paths = pathlib.Path(read_path).iterdir()
    classes_results = {}
    for path in file_paths:
        with open(path, "r") as rf, open(write_path, "w") as wf:
            # Read JSON
            classes_results[path.stem] = defaultdict(list)
            _scores = json.load(rf)
            for _score in _scores:
                for subject, subject_score in _score.items():
                    # Setting defaultdict above is equivalent to below:
                    # classes_results[path.stem].setdefault(subject, [])
                    classes_results[path.stem][subject].append(subject_score)
            # Write to TSV
            writer = csv.writer(wf, delimiter="\t")
            header = ["class", "subject", "min_score", "max_score", "avg_score"]
            writer.writerow(header)
            for _class in classes_results:
                for _subject, _scores in classes_results[_class].items():
                    _min, _max, _avg = (
                        min(_scores),
                        max(_scores),
                        sum(_scores) / len(_scores),
                    )
                    writer.writerow([_class, _subject, _min, _max, _avg])


################################################################################
# Reverse Lines


def reverse_lines(read_path: str, write_path: str) -> None:
    """Reads a text file and writes to another path with the strings reversed.

    Args:
        read_path: Path to text file to read
        write_path: Path to text file to write
    """
    with open(read_path, "r") as rf, open(write_path, "w") as wf:
        for line in rf:
            line = line.rstrip()
            reverse = f"{line[::-1]}\n"
            wf.write(reverse)
