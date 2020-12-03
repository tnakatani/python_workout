def mysum(*args):
    """Reimplement the sum function that comes with Python"""
    num = 0
    for arg in args:
        num += arg
    return num


def mean(*args):
    num = 0
    for arg in args:
        num += 1
    return mysum(*args) / num


def run_timing():
    number_of_runs = 0
    times = []
    while True:
        time = input("Enter 10km run time: ")
        if not time:
            break
        times.append(float(time))
        number_of_runs += 1
    average = mean(*times)
    print(f'Average of {average}, over {number_of_runs} runs')


def to_hex(*args):
    """takes a hex number and returns the decimal equivalent.
    If the user enters 50, you’ll assume that it’s a hex number (equal to 0x50)
    and will print the value 80 to the screen. """
    if not args:
        return args
    decnum = 0
    for i, digit in enumerate(str(args)):
        decnum += int(digit, 16) * (16 ** i)
    return decnum
