from typing import List, Set, Tuple, Dict
import operator
from operator import itemgetter
from collections import Counter, namedtuple


def firstlast(seq):
    """Takes a sequence (string, list, or tuple) and returns
    the first and last elements of that sequence, in a two-element
    sequence of the same type.
    firstlast('abc') -> 'ac'
    """
    # when you retrieve a slice from an object x,
    # you get back a new object of the same type as x
    return seq[:1] + seq[-1:]


def even_odd_sums(seq: List[int]) -> List[int]:
    """ Return a two-element list, containing (respectively) the sum of the even
    -indexed numbers_1 and the sum of the odd-indexed numbers_1
    """
    evens = seq[::2]
    odds = seq[1::2]
    return [sum(evens), sum(odds)]


def plus_minus(seq: List[int]) -> int:
    """ Return the result of alternately adding and subtracting
    numbers_1 from each other"""
    result = seq.pop(0)
    while seq:
        result += seq.pop(0)
        result -= seq.pop(0) if seq else 0
    return result


def mysum(*args):
    """Takes a sequence of numbers_1, strings, lists or tuples and sums them
    together"""
    if not args:
        return args
    result = args[0]
    for arg in args[1:]:
        result += arg
    return result


def sum_numeric(*args):
    """Sums any valid integers passed as an argument"""
    if not args:
        return args
    result = args[0]
    for arg in args[1:]:
        try:
            result += int(arg)
        except ValueError:
            pass
    return result


def alphabetize_names(list_of_dicts: List[Dict]) -> List[Dict]:
    """Returns the list of dicts, but sorted by last name and then by first
    name."""
    return sorted(list_of_dicts,
                  key=itemgetter('last', 'first'))

    # alternate solution
    # return sorted(names, key=lambda names: (names['last'], names['first']))


def count_vowels(list_of_strings: List[str]) -> List[str]:
    """Given a list of strings, sorts them according to how many vowels they
    contain."""
    vowels = 'aeiou'
    vowel_counts = []
    for word in list_of_strings:
        vowel_count = {}
        count = 0
        for letter in word:
            count += 1 if letter in vowels else 0
        vowel_count['word'] = word
        vowel_count['count'] = count
        vowel_counts.append(vowel_count)
    sorted_dict = sorted(vowel_counts, key=itemgetter('count'))
    sorted_list = [x['word'] for x in sorted_dict]
    return sorted_list


def count_vowels_v2(list_of_strings: List[str]) -> List[str]:
    """Given a list of strings, sorts them according to how many vowels they
    contain."""
    vowels = 'aeiou'
    return sorted(list_of_strings, key=lambda word: sum(ch in vowels for ch in
                                                        word))


def sort_summed(list_of_ints: List[List[int]]) -> List[int]:
    """Given a list of lists, with each list containing zero or more numbers,
    sort by the sum of each inner list’s numbers."""
    sorted_nums = sorted(list_of_ints, key=lambda nums: sum(nums))
    return [sum(nums) for nums in sorted_nums]


def most_repeating_letter_count(word: str) -> int:
    """Given a non-empty string, counts how
    many times each letter appears in the string,
    and returns an integer indicating how often
    the most common letter appears."""
    return Counter(word).most_common(1)[0][1]


def most_repeating_word(words: List[str]) -> str:
    """Takes a sequence of strings as input and returns the
    string that contains the greatest number of repeated letters."""
    return max(words, key=most_repeating_letter_count)


def format_sort_records(people: Tuple[str]) -> str:
    """Takes a list of tuples and returns a sorted, tab-separated string"""
    # {1:10} tells Python to display the item with index 1, inserting spaces
    # if the data contains fewer than 10 characters
    template = "{1:10} {0:10} {2:5.2f}"
    output = []
    for person in sorted(people, key=itemgetter(1, 0)):
        print(person)
        output.append(template.format(*person))
    return output


def format_sort_records_v2(list_of_tuples):
    output = []
    template = '{last:10} {first:10} {distance:5.2f}'
    for person in sorted(list_of_tuples, key=operator.attrgetter('last', 'first')):
        # https://docs.python.org/3/tutorial/controlflow.html#unpacking-argument-lists
        output.append(template.format(**(person._asdict())))
    return output

