from typing import Callable


def menu(**kwargs: Callable):
    """Takes any number of key-value pairs as arguments. Each value should be a callable
    When the function is invoked, the user is asked to enter some input. If the user enters a
    string that matches one of the keyword arguments, the function associated with that keyword
    will be invoked, and its return value will be returned to menu’s caller. If the user enters a
    string that’s not one of the keyword arguments, they’ll be given an error message and asked
    to try again.
    """
    # Attempt 1:
    # args = {key: value for key, value in kwargs.items()}
    # while True:
    #     kw = input(f"Enter function keyword from options ({', '.join(args.keys())}): ")
    #     try:
    #         print(args[kw]())
    #     except KeyError:
    #         print(f"Function keyword '{kw}' does not exist. Try again.")

    # Attempt 2:
    while True:
        kw_keys = ', '.join(kwargs)
        kw = input(f"Enter function keyword from options ({kw_keys}): ")
        try:
            return kwargs[kw]()
        except KeyError:
            print(f"Function keyword '{kw}' does not exist. Try again.")
