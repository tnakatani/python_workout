from src.modules.menu.menu import menu


def func_a():
    return "A"


def func_b():
    return "B"


if __name__ == "__main__":
    menu(a=func_a, b=func_b)
