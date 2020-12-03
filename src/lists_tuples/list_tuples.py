from typing import List


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

