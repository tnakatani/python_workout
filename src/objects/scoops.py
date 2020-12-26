from typing import Iterable

"""
In this exercise, you’ll define a class, Scoop, that represents a single scoop of ice cream.
Each scoop should have a single attribute, flavor, a string that you can initialize when you
create the instance of Scoop.

Once your class is created, write a function (create_scoops) that creates three instances of the
Scoop class, each of which has a different flavor
"""


class Scoop:
    def __init__(self, flavor: str):
        self.flavor = flavor


def create_scoops(flavors: Iterable[str]):
    return [Scoop(flavor).flavor for flavor in flavors]


"""
Write a Beverage class whose instances will represent beverages. Each beverage should have two 
attributes: a name (describing the beverage) and a temperature. Create several beverages and 
check that their names and temperatures are all handled correctly.

If no temperature is specified, set default at 75 degrees
"""


class Beverage:
    def __init__(self, name: str, temp: float = 75):
        self.name = name
        self.temp = temp


"""
Create a new LogFile class that expects to be initialized with a filename. Inside of __init__, 
open the file for writing and assign it to an attribute, file, that sits on the instance. Check 
that it’s possible to write to the file via the file attribute.
"""


class LogFile:
    def __init__(self, filename: str):
        self.filename = filename

    def write(self, text: str):
        with open(self.filename, "w") as f:
            f.write(text)
