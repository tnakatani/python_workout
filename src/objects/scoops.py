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


"""
In this exercise, I want you to define a class attribute that will function like a constant, 
ensuring that we don’t need to hardcode any values in our class.

Let’s make the children sad, and their parents happy, by capping the number of scoops in a bowl 
at three. That is, you can add as many scoops in each call to Bowl.add_scoops as you want, 
and you can call that method as many times as you want--but only the first three scoops will 
actually be added. Any additional scoops will be ignored.
"""


@dataclass
class BowlWithLimitedScoops(Bowl):
    # By putting the attribute on the class we indicate that every bowl will have  the same maximum.
    # Dataclass class variables should be annotated with typing.ClassVar.
    # Reference: https://stackoverflow.com/a/57979694/12207563
    max_scoops: ClassVar[int] = 3

    def __post_init__(self):
        super().__init__()

    def add_scoops(self, *new_scoops: ClassVar):
        for scoop in new_scoops:
            if len(self.scoops) < self.max_scoops:
                self.scoops.append(scoop)
            else:
                raise MaxScoopExceeded


class MaxScoopExceeded(Exception):
    pass


"""
1. Define a Person class, and a population class attribute that increases each time you create a 
new instance of Person. Double-check that after you’ve created five instances, named p1 through p5, 
Person.population and p1.population are both equal to 5.
2. Modify your Person class such that when a Person instance is deleted, the population count 
decrements by 1.
"""


@dataclass
class Person:
    population: ClassVar[int] = 0

    def __post_init__(self):
        Person.population += 1

    def __del__(self):
        Person.population -= 1


"""
Define a Transaction class, in which each instance represents either a deposit or a withdrawal 
from a bank account. When creating a new instance of Transaction, you’ll need to specify an 
amount--positive for a deposit and negative for a withdrawal. Use a class attribute to keep track 
of the current balance, which should be equal to the sum of the amounts in all instances created 
to date.
"""


@dataclass
class Transaction:
    balance: ClassVar[int] = 0
    amount: int

    def __post_init__(self):
        Transaction.balance += self.amount


"""Alternative - No dataclass
class Transaction:
    balance = 0

    def __init__(self, amount):
        self.amount = amount
        Transaction.balance += amount
"""

"""
Implement BigBowl for this exercise, such that the only difference between it and the Bowl class 
we created earlier is that it can have five scoops, rather than three. And yes, this means that 
you should use inheritance to achieve this goal.
"""


@dataclass
class BigBowl(BowlWithLimitedScoops):
    max_scoops: ClassVar[int] = 5


"""
Write an Envelope class, with two attributes, weight (a float, measuring grams) and was_sent (a 
Boolean, defaulting to False). There should be three methods: (1) send, which sends the letter, 
and changes was_sent to True, but only after the envelope has enough postage; (2) add_postage, 
which adds postage equal to its argument; and (3) postage_needed, which indicates how much 
postage the envelope needs total. The postage needed will be the weight of the envelope times 10. 
Now write a BigEnvelope class that works just like Envelope except that the postage is 15 times 
the weight, rather than 10.
"""


class Envelope:
    def __init__(self, weight, postage):
        self.weight: float = weight
        self.postage: int = postage
        self.postage_coefficient: int = 10
        self.was_sent: bool = False

    def postage_needed(self):
        """Indicates how much postage the envelope needs in total"""
        return self.weight * self.postage_coefficient

    def send(self):
        """Sends letter and changes was_sent to True, but only if envelope has enough postage"""
        if self.postage >= self.postage_needed():
            self.was_sent = True
        else:
            raise InsufficientPostage


class BigEnvelope(Envelope):
    def __init__(self, weight, postage):
        super().__init__(weight, postage)
        self.postage_coefficient = 15


class InsufficientPostage(Exception):
    pass


"""
Create a Phone class that represents a mobile phone. (Are there still nonmobile phones?) The 
phone should implement a dial method that dials a phone number (or simulates doing so). Implement 
a SmartPhone subclass that uses the Phone.dial method but implements its own run_app method. Now 
implement an iPhone subclass that implements not only a run_app method, but also its own dial 
method, which invokes the parent’s dial method but whose output is all in lowercase as a sign of 
its coolness.
"""


class Phone:
    def __init__(self, phone_number):
        self.full_phone_number: str = phone_number
        self.area_code: str = self.full_phone_number[:3]
        self.phone_number_no_area_code: str = str(self.full_phone_number[3:])

    def validate_phone_number(self):
        raise NotImplemented

    def format_phone_number(self):
        return "-".join(
            [
                self.area_code,
                self.phone_number_no_area_code[:3],
                self.phone_number_no_area_code[3:],
            ]
        )

    def dial(self):
        print(f"Dialing {self.format_phone_number()}")


class SmartPhone(Phone):
    def __init__(self, phone_number):
        super().__init__(phone_number)
        self.app_on = False

    def run_app(self):
        self.app_on = True


class Iphone(SmartPhone):
    spoken_digits: list = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]
    spoken_digit_dict: dict = {i: j for i, j in zip(range(10), spoken_digits)}

    def __init__(self, phone_number):
        super().__init__(phone_number)
        self.phone_number_spoken_form = self.digit_sequence_to_spoken(phone_number)

    # Note: Using a @staticmethod here does not work because I rely on
    # self.spoken_digit_dict
    def digit_to_spoken(self, digit: str) -> str:
        """Simple conversion of 0-9 digits to spoken form"""
        return self.spoken_digit_dict[int(digit)]

    def digit_sequence_to_spoken(self, digit_seq: str):
        return [self.digit_to_spoken(i) for i in digit_seq]

    def dial(self):
        return "-".join(self.phone_number_spoken_form)


"""
Define a Bread class representing a loaf of bread. We should be able to invoke a get_nutrition 
method on the object, passing an integer representing the number of slices we want to eat. In 
return, we’ll receive a dict whose key-value pairs will represent calories, carbohydrates, 
sodium, sugar, and fat, indicating the nutritional statistics for that number of slices. Now 
implement two new classes that inherit from Bread, namely WholeWheatBread and RyeBread. Each 
class should implement the same get_nutrition method, but with different nutritional information 
where appropriate.
"""


class Bread:
    def __init__(self):
        # nutrition per slice
        self.calories = 67
        self.carbohydrates = 13
        self.sodium = 0.144
        self.sugar = 1.4
        self.fat = 1.1

    def get_nutrition(self, number_of_slices):
        return {key: value * number_of_slices for key, value in vars(self).items()}

    """Attempt 1
    nutrition_table: ClassVar[dict] = {
        "calories": 67,
        "carbohydrates (g)": 13,
        "sodium (mg)": 0.144,
        "sugar (g)": 1.4,
        "fat (g)": 1.1,
    }

    def get_nutrition(self, slices: int):
        return {i: j * slices for i, j in self.nutrition_table.items()}
    """


class WheatBread(Bread):
    def __init__(self):
        # nutrition per slice
        self.calories = 80
        self.carbohydrates = 20
        self.sodium = 0.170
        self.sugar = 4
        self.fat = 0
