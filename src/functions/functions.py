import operator
import random
import string
from typing import Callable, List, Tuple


################################################################################
# XML Generator


def myxml(tag: str, content: str = "", **kwargs) -> str:
    """Converts arguments into a XML formatted string.

    Args:
        tag: Name of the tag
        content: Text placed between the opening/closing tags
        *args: Attributes inside of the opening tag

    Returns:
        XML formatted string
    """
    # Attempt 1:
    # if kwargs:
    #     attributes = " " + " ".join(
    #         ["=".join([key, str(value)]) for key, value in kwargs.items()]
    #     )
    # else:
    #     attributes = ""
    # return f"<{tag}{attributes}>{content}</{tag}>"

    # Attempt 2:
    attributes = (
        "".join([f' {key}="{value}"' for key, value in kwargs.items()])
        if kwargs
        else ""
    )
    return f"<{tag}{attributes}>{content}</{tag}>"


def factorial(*args) -> int:
    """Yet another function that takes any number of numeric arguments and returns the result of
    multiplying them all by one another."""
    result = 1
    for arg in args:
        result = result * arg
    return result


################################################################################
# Prefix Notation Calculator


def is_exp(iter: List[str]):
    """Returns true if prefix notation operator is exponentiation (**)"""
    return True if iter[:2] == "**" else False


def calc(formula: str) -> int:
    """Performs prefix notation calculation, ie. operator precedes the arguments.  Handles
    addition, subtraction, multiplication, division (/), modulus (%), and exponentiation (**).

    Args:
        formula: a string containing a simple math expression in prefix notation--with an
        operator and two numbers. Example: "+23" == 5
    """
    ops = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv,
        "%": operator.mod,
        "**": operator.pow,
    }
    # Expontential operator need special handling since it contains 2 chars
    op, num_range = (
        ("**", formula[2:]) if is_exp(formula) else (formula[0], formula[1:])
    )
    nums = [int(num) for num in num_range]
    result = nums[0]
    for num in nums[1:]:
        result = ops[op](result, num)
    return result


################################################################################
# Password Generator


def create_password_generator(text: str) -> Callable:
    """Returns a function that a creates a password of a specified length, using the string
    passed as the argument.

    Args:
        text: strings to be used to create the password
    """

    def password_generator(length: int) -> str:
        chars = []
        for i in range(length):
            chars.append(random.choice(text))
        return "".join(chars)

    return password_generator


def create_password_checker(
    min_uppercase: int, min_lowercase: int, min_punctuation: int, min_digits: int
) -> Callable:
    """Returns a function that checks that a given password meets the minimum occurrence criteria
    for the arguments passed"""

    def count_params(password: str) -> Tuple[int]:
        """Counts the number of occurrences of each acceptance criteria"""
        upper_case, lower_case, punctuation, digit = 0, 0, 0, 0
        for char in password:
            if char.isupper():
                upper_case += 1
            if char.islower():
                lower_case += 1
            if char in string.punctuation:
                punctuation += 1
            if char.isdigit():
                digit += 1
        return digit, lower_case, punctuation, upper_case

    def count_meets_minimum(criteria_counts: Callable) -> bool:
        """Checks whether the counts for each acceptance criteria meets the minimum threshold"""
        for counts, minimum in zip(
            criteria_counts,
            (min_uppercase, min_lowercase, min_punctuation, min_digits),
        ):
            if counts >= minimum:
                continue
            return False
        return True

    def password_checker(password: str):
        return count_meets_minimum(count_params(password))

    return password_checker
