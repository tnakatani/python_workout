from collections import Counter
from typing import Callable, Dict, Iterable, List, Tuple, Union


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
