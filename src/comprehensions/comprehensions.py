import json
import pathlib
import re
import string
from collections import Counter, defaultdict
from typing import Callable, Dict, Iterable, List, Set, Tuple, Union


################################################################################
# Join Numbers


def join_numbers(nums: Iterable[int]) -> str:
    """Given a range of integers, returns those numbers as a string, with commas between the
    numbers.

    Args:
        nums: Range of number, ie. range(15)
    """
    return ", ".join(str(num + 1) for num in nums)


def join_numbers_below_ten(nums: Iterable[int]) -> str:
    """Given a range of integers, returns those numbers as a string, with commas between the
    numbers only if the integer is below 10.

    Args:
        nums: Range of number, ie. range(15)
    """
    return ", ".join(str(num + 1) for num in nums if num < 9)


def reverse_lines_in_file(file_path: str) -> List[str]:
    """Given a file path, read contents of a file and return a list with each line reversed.

    Args:
        file_path: Path to the input file.
    """
    with open(file_path, "r") as fp:
        return [line.strip()[::-1] for line in fp]


def sum_numbers(text_sequence: str) -> int:
    """Given a string of space delimited tokens, sums only the valid integers.

    Args:
        text_sequence: Space delimited sequence of tokens
    """
    return sum(int(token) for token in text_sequence.split() if token.isdigit())


def filter_to_lexically_diverse(file_path: str) -> List[str]:
    """Given a file path, read contents of a file and return a list with lines that contain
     more than 20 unique words.

    Args:
        file_path: Path to the input file.
    """
    with open(file_path, "r") as fp:
        return [line.strip() for line in fp if len(set(line.strip().split())) > 20]


def change_area_code(tel_num: str) -> str:
    """Given a 10 digit telephone number XXX-YYY-ZZZZ, change any phone number whose YYY begins
    with the digits 0-5 to have its area code changed to XXX+1.  Otherwise, return the same number
    as the input.

    Args:
        tel_num: 10 digit telephone in XXX-YYY-ZZZZ format
    """
    # Attempt 1:
    # is_smaller_than_five = int(tel_num.split("-")[1][ 0]) <= 5
    # tel_nums = [int(num) for num in tel_num.split("-")]
    # num4 = [str(num + 1) if num == tel_nums[0] and is_smaller_than_five else str(num) for num
    # in tel_nums]
    # return "-".join(num4)

    # Attempt 2:
    area_code, phone_number = tel_num.split("-", 1)
    return (
        f"{int(area_code) + 1}-{phone_number}"
        if phone_number[0] in "012345"
        else tel_num
    )


################################################################################
# Flatten


def flatten(iters: List[List[Union[int, str]]]) -> List[Union[int, str]]:
    """Takes a list of lists (just one element deep) and returns a flat, one-dimensional version
    of the list.

    Args:
        iters: List of lists
    """
    return [one_elem for one_list in iters for one_elem in one_list]


def flatten_odd_ints(iters: List[List[Union[int, str]]]) -> List[int]:
    """Takes a list of lists (just one element deep) and returns a flat, one-dimensional version
    of the list. Output will only contain odd integers. Inputs that are neither odd nor integers
    are excluded. Inputs containing strings that could be converted to integers should be
    converted; other strings should be excluded

    Args:
        iters: List of lists
    """
    # Attempt in regular loop form
    # f = []
    # for iter in iters:
    #     for i in iter:
    #         if str(i).isdigit() and int(i) % 2 == 1:
    #             f.append(i)
    # return f
    return [
        int(i) for iter in iters for i in iter if str(i).isdigit() and int(i) % 2 == 1
    ]


def get_children(tree: Dict[str, List[str]]) -> List[str]:
    """Reads a dict that represents the children and grandchildren in a family. Each key will be a
    child’s name, and each value will be a list of strings representing their children (i.e.,
    the family’s grandchildren). Returns a list of each grandchildren.

    Args:
        tree: dict that represents the children and grandchildren in a family
    """
    return [elem for _, v in tree.items() for elem in v]


def sort_children_by_oldest(
    tree: Dict[str, List[Dict[str, Union[int, str]]]]
) -> List[str]:
    """Reads a dict that represents the children and grandchildren in a family. Each key will be a
    child’s name, and each value will be a list of strings representing their children (i.e.,
    the family’s grandchildren). Returns a list of dicts, with each dict containing two
    name-value pairs, 'name' and 'age'. Returns a list of the grandchildren’s names, sorted by
    age, from eldest to youngest

    Args:
        tree: dict that represents the children and grandchildren in a family
    """
    # 1. Flatten dicts of all children into list
    result = [elem for _, v in tree.items() for elem in v]
    # 2. Sort list by 'age' key
    result = sorted(result, key=lambda x: x["age"], reverse=True)
    # 3. Extract the grandchildren name from each dict
    return [d["name"] for d in result]


################################################################################
# Pig Latin


def plfile(file_path: str) -> str:
    """Takes filename as an argument and returns a string with the file’s contents, but with
    each word translated into Pig Latin, as per our plword function in chapter 2 on “strings.”
    The returned translation ignores newlines and doesn't handle capitalization and
    punctuation in any specific way.

    Args:
        file_path: Path to file
    """
    with open(file_path, "r") as f:
        result = " ".join(
            word + "way" if word[0] in "aeiou" else word[1:] + word[0] + "ay"
            for line in f
            for word in line.rstrip().split(" ")
        )
        return result


def to_pig_latin(string: str) -> str:
    """Reads a string an returns the pig latin form

    Args:
        string: a string sequence, e.g. "hello"
    """
    return string + "way" if string[0] in "aeiou" else string[1:] + string[0] + "ay"


def cap_every_odd_letter(string: str) -> str:
    """Capitalizes every other letter in the string argument.

    Args:
        string:
    """
    return "".join(
        letter.upper() if (i + 1) % 2 == 1 else letter.lower()
        for i, letter in enumerate(string)
    )


def funcfile(file_path: str, func: Callable) -> str:
    """Take two arguments--a filename and a function. Reads the text file from the file path and
    invokes the function on each word in the text file.

    Args:
        file_path: Path to file
        func: Function invoked on each word in the file
    """
    with open(file_path, "r") as f:
        result = " ".join(func(word) for line in f for word in line.rstrip().split(" "))
        return result


def dict_to_list_of_tuples(list_of_dicts: List[Dict[str, str]]) -> List[Tuple[str]]:
    """Transforms a list of dicts into a list of two-element (name-value) tuples, each of which
    represents one of the name-value pairs in one of the dicts. If more than one dict has the
    same name-value pair, then the tuple appears twice.

    Args:
        list_of_dicts: List of dictionary objects
    """
    return [(k, v) for dict_obj in list_of_dicts for k, v in dict_obj.items()]


def get_most_common_score(list_of_dicts: List[Dict[str, List[int]]]):  # -> List[int]:
    """Reads a list of dicts, in which each dict contains two name-value pairs: name and values,
    where name is the person’s name and values is a list of strings representing the person’s
    test scores. Returns the the 3 most common scores among the people listed in the dicts.

    Args:
        list_of_dicts: List of dictionary object, each containing a username and list of scores.
    """
    return Counter(
        score
        for dict_obj in list_of_dicts
        for _, scores in dict_obj.items()
        for score in scores
    ).most_common(3)


################################################################################
# Flip Dict


def flip_dict(dict_obj: Dict[any, any]) -> Dict[any, any]:
    """Given a dictionary object, returns the object with keys and values inverted"""
    return {v: k for k, v in dict_obj.items()}


def count_vowels(word: str) -> int:
    """Returns the number of vowels in a word"""
    # Attempt 1:
    # count = 0
    # for char in word:
    #     if char in "aeiou":
    #         count += 1
    # Attempt 2:
    return sum(1 for char in word if char in "aeiou")


def get_vowel_count(words: str) -> Dict[str, int]:
    """Given a string containing several (space-separated) words, create a dict in which the keys
    are the words, and the values are the number of vowels in each word.

    Args:
        words: strings containing words
    """
    return {word: count_vowels(word) for word in words.split(" ")}


##########################################################################################
# Transform Values


def transform_values(func: Callable, dict_obj: Dict[str, int]) -> Dict[str, int]:
    """Emulates the map function, but applies it to the value of the values in a dictionary object.

    Args:
        func: Function passed as an argument
        dict_obj: Dictionary object with string keys and integer values
    """
    return {k: func(v) for k, v in dict_obj.items()}


def get_filename_and_size(dir: str) -> Dict[str, int]:
    """Takes a directory name (i.e., a string) as an argument. Returns a dict
    in which the keys are the names of files in that directory, and the values are the file sizes.

    Args:
        dir: Path to directory
    """
    return {
        pathlib.Path(fp).name: pathlib.Path(fp).stat().st_size
        for fp in pathlib.Path(dir).iterdir()
    }


################################################################################
# Supervocalic


def get_supervocalic(words: str) -> Tuple[str]:
    """From a sentence, finds all words that contain all vowels (a, e, i, o,and u) and return a set
    of those words.

    Args:
        words: sequence of words
    """
    # Attempt 1:
    # l = []
    # for word in words.split(" "):
    #     if {"a", "e", "i", "o", "u"} < set(chars for chars in word):
    #         l.append(word)
    # return l

    # Attempt 2:
    return tuple(
        word
        for word in words.split(" ")
        if {"a", "e", "i", "o", "u"} < set(chars for chars in word)
    )


def contain_keywords(words: str, kw: List[str]) -> bool:
    """From a sentence, checks if all the keywords exist in the sentence.

    Args:
        words: sequence of words
    """
    return True if {k for k in kw} < set(words.split(" ")) else False


def get_passwd_shells(file_path: str) -> Set[str]:
    """Reads a /etc/passwd and returns a tuple of all unique shells assigned to users

    Args:
        file_path: Path to file
    """
    with open(file_path, "r") as f:
        return set(
            line.strip().split(":")[-1]
            for line in f
            if line.strip() and "#" not in line[0]
        )


def get_word_lengths(file_path: str) -> Dict[int, Set[str]]:
    """Reads a text file and returns a dictionary where the keys are the character length of words
    and its value is an iterable that contains all unique words that have the key's character
    length.

    Args:
        file_path: Path to file
    """

    # Attempt 1: Seems like this is not easily done with a comprehension, as it needs
    # to initiialize a defaultdict
    def normalize(word: str) -> str:
        """Basic word token normalization (remove punctuation except apostrophe, lowercase)"""
        return re.sub(r"[^\w\d']+", "", word).lower()

    with open(file_path, "r") as f:
        lengths = defaultdict(set)
        for line in f:
            for word in line.strip().split(" "):
                lengths[len(word)].add(normalize(word))
        return lengths


################################################################################
# Genatria pt. 1


def make_gematria() -> Dict[int, str]:
    """Create a dict whose keys are the (lowercase) letters of the English alphabet, and whose
    values are the numbers ranging from 1 to 26.
    """
    return {char: i for i, char in enumerate(string.ascii_lowercase[:27], 1)}


def config_to_dict(file_path: str) -> Dict[str, Union[str, int]]:
    """Convert a config file where each line of the file contains text in the form of "name=value"
    into a "name: value" dictionary.

    Args:
        file_path: Path to file
    """
    # Not really worth turning this into a comprehension... difficult to read
    with open(file_path, "r") as f:
        return {
            config.strip().split("=")[0]: int(config.strip().split("=")[1])
            # convert value to int if digit, else keep as string
            if config.strip().split("=")[1].isdigit() else config.strip().split("=")[1]
            for config in f
        }


def get_city_populations(file_path: str) -> Dict[str, int]:
    """Reads a city data JSON file and returns a dict in which the keys are the city names,
    and the values are the populations of those cities.

    Args:
        file_path: Path to city data JSON
    """
    with open(file_path, "r") as f:
        result = {
            dict_obj["city"]: int(dict_obj["population"]) for dict_obj in json.load(f)
        }
        return result


################################################################################
# Genatria pt. 2

GEMATRIA = make_gematria()


def gematria_for(word: str) -> int:
    """Takes a single word as an argument and returns the gematria score for that word.
    The gematria scoring is capitalization agnostic, ie. "A" and "a" both get 1.

    Args:
        word: single word token
    """
    # Attempt 1:
    # return sum(GEMATRIA[char] for char in word)

    # Attempt 2
    return sum(GEMATRIA.get(char.lower(), 0) for char in word)


def gematria_equal_words(file_path: str, word: str) -> List[str]:
    with open(file_path, "r") as f:
        return [line.strip() for line in f if gematria_for(line) == gematria_for(word)]


def convert_book_data_to_dict(
    book_data: List[Tuple[Union[str, float]]]
) -> Dict[str, Dict[str, Union[str, float]]]:
    """Turn a list of tuples with book data into a dict whose keys are the book’s
    titles, with the values being another (sub -) dict, with keys for (a) the author’s first
    name, (b) the author’s last name, and (c) the book’s price in U.S. dollars.


    Args:
        book_data: List of tuples in which each tuple contains three elements: (1) the author’s
    first and last names, (2) the book’s title, and (3) the book’s price in U.S. dollars.
    """
    return {
        title: {
            "first_name": author.split()[0],
            "last_name": author.split()[1],
            "price": price,
        }
        for author, title, price in book_data
    }
