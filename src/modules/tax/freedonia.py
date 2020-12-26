from decimal import Decimal

PROVINCES = {
    "Chico": Decimal("0.5"),
    "Groucho": Decimal("0.7"),
    "Harpo": Decimal("0.5"),
    "Zeppo": Decimal("0.4"),
}

# Attempt 1:
# HOUR_TO_TAX = {i: Decimal(i * 1 / 24) for i in range(24)}

# Attempt 2:
def hour_to_tax(hour: int) -> Decimal:
    return hour / Decimal("24.0")


class HourException(Exception):
    pass


def calc_price_with_tax(price: float, province: str, hour: int) -> Decimal:
    """Takes three arguments: the amount of the purchase, the province in which the purchase took
    place, and the hour (an integer, from 0-24) at which it happened. The calculate_tax function
    should return the final price, as a float.

    Args:
        price: Price of purchase
        province: Province where purchase was made
        hour: The hour (in 24-hour format) when the purchase was made
    """
    if hour < 0:
        raise HourException("hour argument requires integer between 0 and 24")
    if hour > 24:
        raise HourException("hour argument requires integer between 0 and 24")
    tax = price * PROVINCES[province] * hour_to_tax(hour)

    # Return float at last possible moment
    return float(price + tax)
