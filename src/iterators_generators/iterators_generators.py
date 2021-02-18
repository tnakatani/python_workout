####################################################################################################
# e47: MyEnumerate

"""
Create your own MyEnumerate class, such that someone can use it instead of enumerate. It will
need to return a tuple with each iteration, with the first element in the tuple being the index (
starting with 0) and the second element being the current element from the underlying data
structure. Trying to use MyEnumerate with a noniterable argument will result in an error.

BTE 1: Rewrite MyEnumerate such that it uses a helper class (MyEnumerateIterator). MyEnumerate
       will have the __iter__ method that returns a new instance of MyEnumerateIterator,
       and the helper
       class will implement __next__.
BTE 2: Add a second, optional argument--an integer, representing the first index that should be
       used.  This is handy for implementing one-indexed arrays.
"""


class MyEnumerate:
    def __init__(self, data, start: int = 0):
        self.data = data
        self.index = 0

    def __iter__(self):
        return MyEnumerateIterator(self.data)


class MyEnumerateIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration

        value = (self.index, self.data[self.index])
        self.index += 1
        return value


# BTE 3: Redefine MyEnumerate as a generator function, rather than as a class.
def my_generator(data, start: int = 0):
    index = start
    for i in data:
        yield (index, data[index])
        index += 1


####################################################################################################
# e47: Circle

"""
Define a class, Circle, that takes two arguments when defined: a sequence and a number. The idea 
is that the object will then return elements the defined number of times. If the number is 
greater than the number of elements, then the sequence repeats as necessary. You should define 
the class such that it uses a helper (CircleIterator). Here’s an example:

c = Circle('abc', 5)
print(list(c)) # ['abcab']
"""


class Circle:
    def __init__(self, data, end: int = 0):
        self.data = data
        self.index = 0
        self.end = end if end else len(self.data)

    def __iter__(self):
        return CircleIterator(self.data, self.end)


class CircleIterator:
    def __init__(self, data, end: int = 0):
        self.data = data
        self.index = 0
        self.end = end if end else len(self.data)

    def __next__(self):
        if self.index >= self.end:
            raise StopIteration

        # Modulo is often used in programs to ensure that we can wrap around as many times as we
        # need.
        value = self.data[self.index % len(self.data)]
        self.index += 1
        return value


"""
BTE 1: Reimplement Circle as a class that inherits from CircleIterator, which implements 
__init__ and __next__. Of course, the parent class will have to know what to return in each 
iteration; add a new attribute in Circle, self.returns, a list of attribute names that should 
be returned.
BTE 1: Reimplement Circle as a class that inherits from CircleIterator, which implements 
__init__ and __next__. Of course, the parent class will have to know what to return in each 
iteration; add a new attribute in Circle, self.returns, a list of attribute names that should 
be returned.
"""


class Circle_2:
    def __init__(self, data, end: int = 0):
        self.data = data
        self.index = 0
        self.end = end if end else len(self.data)

    def __next__(self):
        if self.index >= self.end:
            raise StopIteration

        iterated_data = getattr(self, self.returns)

        # Modulo is often used in programs to ensure that we can wrap around as many times as we
        # need.
        value = iterated_data[self.index % len(iterated_data)]
        self.index += 1
        return value

    def __iter__(self):
        return type(self)(self.data, self.end)


class CircleInherit(Circle_2):
    def __init__(self, data, end: int = 0):
        super().__init__(data, end)
        self.returns = "data"


"""
BTE 2: Implement Circle as a generator function, rather than as a class.
"""


def my_generator(data, start: int = 0):
    index = start
    for i in data:
        yield (index, data[index])
        index += 1


def circle(data, end: int = 0):
    index = 0
    while end:
        yield (data[index % len(data)])
        index += 1
        end -= 1


"""
BTE 3: Implement a MyRange class that returns an iterator that works the same as range, at least 
in for loops. (Modern range objects have a host of other capabilities, such as being 
subscriptable. Don’t worry about that.) The class, like range, should take one, two, or three 
integer arguments.
"""

class MyRange:
    def __init__(self, start: int = 0, stop: int = 0, step: int = 1):
        self.start = start
        self.stop = stop
        self.step = step

    def __iter__(self):
       return self

    def __next__(self):
        if self.start >= self.stop:
            raise StopIteration
        value = self.start
        self.start += self.step
        return value
