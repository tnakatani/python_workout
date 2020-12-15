from collections import Counter, defaultdict, OrderedDict
from datetime import datetime, timedelta
import os
from typing import Dict, Set, List, Union, Callable, Tuple
from functools import reduce

MENU = {"sandwich": 9.99, "fries": 2.99, "coffee": 1.99, "pancakes": 6.99}

TEMPS = {
    "11/29/2020": 40,
    "11/30/2020": 49,
    "12/01/2020": 40,
    "12/02/2020": 52,
    "12/03/2020": 55,
}


######################################################################
# Menu Items Exercise


def normalize(text: str) -> str:
    """Lower case and strip spaces"""
    return text.lower().strip()


def restaurant(menu: Dict[str, float]) -> None:
    """Asks the user to enter an order:
    - If the user enters the name of a dish on the menu, the program prints the
    price and the running total. It then asks the user again for their order.
    - If the user enters the name of a dish not on the menu, the program
     scolds the user (mildly). It then asks the user again for their order.
    - If the user enters 'done', prints the total price.
    """
    total = 0
    while True:
        item = normalize(input('Order (type "done" to complete order): '))
        if not item:
            print("You didn't order anything...")
        if item == "done":
            print(f"Your total is {total}")
            break
        else:
            if item in menu:
                item_price = menu[item]
                total += item_price
                print(f"{item} costs {item_price}, total is {total}")
            else:
                print(f"Sorry, we are fresh out of {item}")


######################################################################
# Date Temperature Exercise


def get_yesterday_and_tomorrow_date(day: str) -> str:
    """Takes a date string in MM/DD/YYYY format and returns the date 1 day
    before/after in the same format"""
    _date = datetime.strptime(day, "%m/%d/%Y")
    yesterday = (_date.date() - timedelta(days=1)).strftime("%m/%d/%Y")
    tomorrow = (_date.date() + timedelta(days=1)).strftime("%m/%d/%Y")
    return yesterday, tomorrow


def get_temp_by_date(temps: Dict[str, int]) -> None:
    """Asks the user to enter a date, and display the temperature on that
    date, as well as the previous and subsequent dates, if available."""
    while True:
        date = normalize(input('Select date (type "done" to complete): '))
        if not date:
            print("No query registered, try again.")
        if date == "done":
            break
        else:
            if date not in temps:
                print(f"Date not found, try again.")
                continue
            yesterday, tomorrow = get_yesterday_and_tomorrow_date(date)
            try:
                yesterday_temp = temps[yesterday]
                tomorrow_temp = temps[tomorrow]
            except KeyError:
                print("Date range is out of bounds, try again.")
                continue
            temp = temps[date]
            print(f"{yesterday} temperature: {yesterday_temp}")
            print(f"{date} temperature: {temp}")
            print(f"{tomorrow} temperature: {tomorrow_temp}")


######################################################################
# Rainfall Exercise


def dict_is_empty(_dict: Dict) -> bool:
    return bool(_dict) == False


def rainfall_report() -> None:
    """Tracks rainfall in a number of cities.
    - Users is prompted to enter the name of a city;
    - If the city name is blank, then the function prints a report before
    exiting.
    - If the city name isn’t blank, then the program asks the
    user how much rain has fallen in that city (in millimeters).
    - After the user enters the quantity of rain, the program again asks
    them for a city name, rainfall amount, and so on--until the user presses
    Enter instead of typing the name of a city.

    Example output:
    Boston: 10
    New York: 7
    """
    report = {}
    while True:
        city = normalize(input("Enter the name of a city: ")).capitalize()
        if not city:
            break
        rainfall = normalize(
            input(f"Enter the reported rainfall in" f" {city} (in millimeters): ")
        )
        if rainfall.isdigit():
            rainfall = int(rainfall)
        else:
            print("Not a valid value, try again.")
            continue
        # with two arguments, dict.get returns either the value associated
        # with the key or the second argument
        report[city] = report.get(city, 0) + rainfall
    if dict_is_empty(report):
        print("No data registered.")
    else:
        print("Reported rainfall:")
        for k, v in report.items():
            print(f"{k}: {v}mm")


######################################################################
# Word Length Counter


def tokenize(text: List[str]) -> List[str]:
    """Takes in a list of newline delimited text and returns a list of string
    tokens"""
    # Remove newlines
    text = [l.rstrip() for l in text]
    # Remove full-width whitespace
    text = [l.replace("\u3000", " ") for l in text]
    # Split by white space
    text = [l.split(" ") for l in text]
    # Flatten list of lists
    tokenized = reduce(lambda x, y: x + y, text)
    # Above is equivalent to:
    # for line in text:
    #     for token in line:
    #         tokens.append(token)
    # Or:
    # tokens = [token for line in text for token in line]
    return tokenized


def word_length_freq_table(file_path: str) -> Dict[int, int]:
    """Read through a text file on disk. Use a dict to track how many words
    of each length are in the file--that is, how many three-letter words,
    four-letter words, five-letter words, and so on."""
    with open(file_path, "r", encoding="utf8") as f:
        lines = f.readlines()
        tokenized = tokenize(lines)
        word_length = {}
        for token in tokenized:
            chars = len(token)
            word_length[chars] = word_length.get(chars, 0) + 1
        return word_length


################################################################################
# Dict Diff


def dictdiff(
    first: Dict[any, any], second: Dict[any, any]
) -> Dict[any, Union[any, List[any]]]:
    """Takes two dicts as arguments. The function returns a new dict that
    expresses the difference between the two dicts.
    - If there are no differences between the dicts, returns an empty
    dict.
    - For each key-value pair that differs, returns a key-value pair in which
    the value is a list containing the values from the two different dicts.
    - If one of the dicts doesn’t contain that key, it should contain None
    """
    output = {}
    all_keys = first.keys() | second.keys()
    for key in all_keys:
        f, s = first.get(key), second.get(key)
        if f != s:
            output[key] = [f, s]
    return output


################################################################################
# Dict Merge


def dictmerge(*args) -> Dict[any, any]:
    """Takes any number of dicts and returns a dict that reflects the
    combination of all of them. If the same key appears in more than one
    dict, then the most recently merged dict’s value appears in the output."""
    output = {}
    for arg in args:
        output.update(arg)
    return output


################################################################################
# Dict Partition


def is_even(v: int) -> bool:
    return v % 2 == 0


def dictpartition(
    d: Dict[any, any], f: Callable
) -> Tuple[Dict[any, any], Dict[any, any]]:
    """Return two dicts, each containing key-value pairs from d. The decision
    regarding where to put each of the key-value pairs will be made according
    to the output from f, which will be run on each key-value pair in d. If f
    returns True, then the key-value pair will be put in the first output
    dict. If f returns False, then the key-value pair will be put in the
    second output dict."""
    output_1, output_2 = {}, {}
    for key in d:
        v = d.get(key)
        if f(v):
            output_1[key] = v
            continue
        output_2[key] = v
    return output_1, output_2


################################################################################
# Different Numbers


def get_unique_integers(numbers: List[int]) -> int:
    """Takes a single list of integers and returns the number of different
    integers it contains"""
    return len(set(numbers))
