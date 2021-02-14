from dataclasses import dataclass, field
from typing import ClassVar, Iterable, List
from uuid import uuid4

####################################################################################################
# e38: Ice cream scoop
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


####################################################################################################
# BTE: Beverage
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


####################################################################################################
# BTE: LogFile
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


####################################################################################################
# e29: Ice cream bowl
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


####################################################################################################
# BTE: Book
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


####################################################################################################
# BTE: Person
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


####################################################################################################
# BTE: Transaction
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

####################################################################################################
# e41: A bigger bowl
"""
Implement BigBowl for this exercise, such that the only difference between it and the Bowl class 
we created earlier is that it can have five scoops, rather than three. And yes, this means that 
you should use inheritance to achieve this goal.
"""


@dataclass
class BigBowl(BowlWithLimitedScoops):
    max_scoops: ClassVar[int] = 5


####################################################################################################
# BTE: Envelope

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


####################################################################################################
# BTE: Phone
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


####################################################################################################
# BTE: Bread

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


####################################################################################################
# e42: Flexible Dict

"""
Implement a subclass of dict called FlexibleDict. Dict keys are Python objects, 
and as such are identified with a type. So if you use key 1 (an integer) to store a value, 
then you can’t use key '1' (a string) to retrieve that value. But FlexibleDict will allow for 
this. If it doesn’t find the user’s key, it will try to convert the key to both str and int 
before giving up.

Cautionary note: This approach of allowing a language to guess a type is very un-Pythonic.
Not recommended in production applications.
"""


class FlexibleDict(dict):
    def __getitem__(self, key):
        """Find dictionary keys regardless of key type (str or int)."""
        try:
            if key in self:
                pass
            elif str(key) in self:
                key = str(key)
            elif int(key) in self:
                key = int(key)
        except ValueError:
            pass

        # Call parent method + __getitem__. Using self.__getitem__ will lead to an infinite loop
        return dict.__getitem__(self, key)

    # Attempt 1 (does not work)
    # def __getitem__(self, key):
    #     try:
    #         return flexibledict[key]
    #     except valueerror:
    #         pass


####################################################################################################
# BTE: StringKeyDict

"""
Implement StringKeyDict, which converts its keys into strings as part of the assignment. Thus, 
immediately after saying skd[1] = 10, you would be able to then say skd['1'] and get the value of 
10 returned. This can come in handy if you’ll be reading keys from a file and won’t be able to 
distinguish between strings and integers.
"""


class StringKeyDict(dict):
    def __setitem__(self, key, value):
        dict.__setitem__(self, str(key), value)

    # Attempt 1: No need to change getitem. Just need to change setitem
    # def __getitem__(self, key):
    #     """Converts its keys into strings as part of the assignment."""
    #     try:
    #         if key in self:
    #             pass
    #         elif str(key) in self:
    #             dict.__setitem__(self, str(key), key)
    #             key = str(key)
    #         elif int(key) in self:
    #             key = int(key)
    #     except ValueError:
    #         pass
    #
    #     return dict.__getitem__(self, key)


####################################################################################################
# BTE: RecentDict

"""
Implement RecentDict. RecentDict class works just like a dict, except that it contains a 
user-defined number of key-value pairs, which are determined when the instance is created. In a 
RecentDict(5), only the five most recent key-value pairs are kept; if there are more than five 
pairs, then the oldest key is removed, along with its value.
"""


class RecentDict(dict):
    def __init__(self, maxsize):
        super().__init__()
        self.maxsize = maxsize

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)

        if len(self) > self.maxsize:
            self.pop(list(self.keys())[0])

    """
    Attempt 1
    Lessons learned: Fails with TypeError: 'int' object is not callable.
    Remember, self.maxsize is an attribute, not a method!
    """
    # def __setitem__(self, key, value):
    #     dict.__setitem__(self, key, value)
    #
    #     if len(self) > self.maxsize():
    #         self.pop(list(self.keys()[0]))


####################################################################################################
# BTE: FlatList


"""
Create the FlatList class. FlatList class inherits from list and overrides the append method. If 
append is passed an iterable, then it should add each element of the iterable separately. This 
means that fl.append([10, 20, 30]) would not add the list [10, 20, 30] to fl, but would rather 
add the individual integers 10, 20, and 30.
"""


class FlatList(list):
    def append(self, __object) -> None:
        try:
            for o in __object:
                list.append(self, o)
        except TypeError:
            list.append(self, __object)

    # Attempt 1: list needs to append to self the __object, else it throws
    # "TypeError: descriptor 'append' for 'list' objects doesn't apply to a 'int' object"
    # def append(self, __object) -> None:
    #     if isinstance(__object, list):
    #         for o in __object:
    #             list.append(o)


####################################################################################################
# e43: Animals

"""
Create an animal class and additional subclasses for animal types. Each type should have attributes:
1. species
2. color
3. number_of_legs
4. print() function that summarizes the above
"""


class Animal:
    def __init__(self, color):
        # Turn the current class object into a string
        self.species: str = self.__class__.__name__
        self.color: str = color

    def __repr__(self):
        return f"{self.color} {self.species}, {self.number_of_legs} legs".lower()


class Wolf(Animal):
    number_of_legs = 4
    space_required = 1100

    def __init__(self, color):
        super().__init__(color)


class Sheep(Animal):
    number_of_legs = 4
    space_required = 700

    def __init__(self, color):
        super().__init__(color)


class Snake(Animal):
    number_of_legs = 0
    space_required = 10

    def __init__(self, color):
        super().__init__(color)


class Parrot(Animal):
    number_of_legs = 2
    space_required = 30

    def __init__(self, color):
        super().__init__(color)


####################################################################################################
# e44: Cages

"""
Create a Cage class to put the Animal class into.  Specifications:
- Upon instantiation, it will have a unique ID
- Has add_animal() method that can pass any number of Animal classes.
- Extends __repr__ method so that printing a cage prints not just the cage ID, but also each of 
the animals it contains.

BTE add-on specifications:
- Add a limit on how many animals can be added to a cage.
- Modify each of the Animal subclasses to include a space_required attribute. Then modify the 
Cage class to reflect how much space each one has. Adding more animals than the cage can contain 
should raise an exception.
- Define a dict describing which animals can be with others. The keys in the dict will be 
classes, and the values will be lists of classes that can compatibly be housed with the keys. 
Then, when adding new animals to the current cage, you’ll check for compatibility. Trying to add 
an animal to a cage that already contains an incompatible animal will raise an exception.
"""

COMPATIBLE_ANIMALS = {
    Wolf: [Wolf],
    Sheep: [Sheep, Snake, Parrot],
    Snake: [Snake, Parrot],
    Parrot: [Parrot, Sheep, Wolf],
}


class Cage:
    def __init__(self, max_capacity: int, max_space: int = 500):
        # use uudi4 module to create a random id
        self.id: str = uuid4()
        self.animals: List[str] = []
        self.max_capacity: int = max_capacity
        self.max_space: int = max_space

    def add_animals(self, *args):
        """Check whether list of animals meets validation requirements. If all pass,
        add all animals"""
        if self.validate_requirements(args):
            [self.animals.append(arg) for arg in args]
        else:
            print("foobar")

    def validate_requirements(self, list_of_animals):
        """Run gauntlet of validation methods"""
        if not any(
            [
                validation_func(list_of_animals)
                for validation_func in [
                    self.exceeds_capacity,
                    self.exceeds_space_required,
                    self.incompatible_animals,
                ]
            ]
        ):
            return True

    def exceeds_capacity(self, list_of_animals: List[classmethod]):
        if len(list_of_animals) > self.max_capacity:
            raise MaxCapacityExceeded(
                f"Animal capacity at len(list_of_animals). Cannot exceed max capacity of"
                f" {self.max_capacity}"
            )
        else:
            return False

    def exceeds_space_required(self, list_of_animals: List[classmethod]):
        total_space_required = sum(a.space_required for a in list_of_animals)
        if total_space_required > self.max_space:
            raise MaxSpaceExceeded(
                f"Total animal space required at {total_space_required}. Cannot exceed max space "
                f"of {self.max_space}"
            )
        else:
            return False

    def incompatible_animals(self, list_of_animals: List[classmethod]):
        for a in set(list_of_animals):
            for b in set(list_of_animals):
                if type(a) not in COMPATIBLE_ANIMALS[type(b)]:
                    raise IncompatibleAnimals(
                        f"{a.__class__.__name__} can not live with {b.__class__.__name__}"
                    )
        return False

    def __repr__(self):
        result = f"{self.id}: \n"
        result += "\n".join(a.species for a in self.animals)
        return result


class MaxCapacityExceeded(Exception):
    pass


class MaxSpaceExceeded(Exception):
    pass


class IncompatibleAnimals(Exception):
    pass


####################################################################################################
# e45: Zoo

"""
- Given a zoo z, we should be able to print all of the cages (with their ID numbers) and the 
animals inside simply by invoking print(z).
- We should be able to get the animals with a particular color by invoking the method 
z.animals_by_color. For example, we can get all of the black animals by invoking 
z.animals_by_color('black'). The result should be a list of Animal objects.
- We should be able to get the animals with a particular number of legs by invoking the method 
z.animals_by_legs. For example, we can get all of the four-legged animals by invoking 
z.animals_by_legs(4). The result should be a list of Animal objects.
- Finally, we have a potential donor to our zoo who wants to provide socks for all of the animals. 
Thus, we need to be able to invoke z.number_of_legs() and get a count of the total number of legs 
for all animals in our zoo.
"""


class Zoo:
    def __init__(self):
        self.cages: List[classmethod] = []

    def add_cages(self, *args):
        [self.cages.append(cage) for cage in args]

    def __repr__(self):
        """Print all of the cages (with their ID numbers) and the animals inside"""
        output = ""
        for cage in self.cages:
            output += f"Cage ID: {str(cage.id)}\n"
            output += "\n".join(str(a) for a in cage.animals)
            output += "\n\n"
        return output

    def animals_by_color(self, color):
        """Filter animals by their color"""
        return [
            animal
            for cage in self.cages
            for animal in cage.animals
            if animal.color == color
        ]

    def animals_by_legs(self, number_of_legs):
        return [
            animal
            for cage in self.cages
            for animal in cage.animals
            if animal.number_of_legs == number_of_legs
        ]

    def total_legs(self):
        result = sum(
            animal.number_of_legs for cage in self.cages for animal in cage.animals
        )
        return result
