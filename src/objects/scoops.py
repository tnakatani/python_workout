from dataclasses import dataclass, field
from typing import ClassVar, Iterable, List

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


"""
In the previous exercise, we created a Scoop class that represents one scoop of ice cream. If 
we’re really going to model the real world, though, we should have another object into which we 
can put the scoops. I thus want you to create a Bowl class, representing a bowl into which we can 
put our ice cream, for example:

s1 = Scoop('chocolate')
s2 = Scoop('vanilla')
s3 = Scoop('persimmon')

b = Bowl()
b.add_scoops(s1, s2)
b.add_scoops(s3)
print(b)
"""


class Bowl:
    def __init__(self) -> None:
        self.scoops: list[ClassVar] = []

    def add_scoops(self, *new_scoops: ClassVar):
        for scoop in new_scoops:
            self.scoops.append(scoop)

    def __repr__(self):
        return "\n".join(scoop.flavor for scoop in self.scoops)


"""
1. Create a Book class that lets you create books with a title, author, and price. Then create a 
Shelf class, onto which you can place one or more books with an add_book method. Finally, 
add a total_price method to the Shelf class, which will total the prices of the books on the shelf.
2. Write a method, Shelf.has_book, that takes a single string argument and returns True or False, 
depending on whether a book with the named title exists on the shelf.
3. Modify your Book class such that it adds another attribute, width. Then add a width attribute to 
each instance of Shelf. When add_book tries to add books whose combined widths will be too much 
for the shelf, raise an exception.

Try replacing __init__ method with dataclasses, which are available on python 3.7 and above.
"""


@dataclass
class Book:
    author: str
    title: str
    price: float
    width: int


@dataclass
class Shelf:
    books: List[Book] = field(default_factory=list)
    width: int = 24

    def add_books(self, *books: Book):
        for book in books:
            if self.total_width_of_books() + book.width > self.width:
                raise WidthTooLargeError
            else:
                self.books.append(book)

    def total_price(self):
        return sum(book.price for book in self.books)

    def has_book(self, book):
        return True if book.lower() in [b.title.lower() for b in self.books] else False

    def total_width_of_books(self):
        return sum(b.width for b in self.books)


class WidthTooLargeError(Exception):
    """Raised when the total width of the books are too wide for the shelf"""
    pass
