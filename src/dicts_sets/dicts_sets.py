from collections import Counter, defaultdict

MENU = {'sandwich': 9.99,
        'fries': 2.99,
        'coffee': 1.99,
        'pancakes': 6.99}


def normalize(text: str) -> str:
    """Lower case and strip spaces"""
    return text.lower().strip()


def restaurant(menu):
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

