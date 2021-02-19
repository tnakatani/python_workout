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
import os
from typing import Iterable, List


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
    for index in range(end):
        yield data[index % len(data)]

    # Attempt 1:
    # index = 0
    # while end:
    #     yield (data[index % len(data)])
    #     index += 1
    #     end -= 1


"""
BTE 3: Implement a MyRange class that returns an iterator that works the same as range, at least 
in for loops. (Modern range objects have a host of other capabilities, such as being 
subscriptable. Don’t worry about that.) The class, like range, should take one, two, or three 
integer arguments.
"""


class MyRange:
    def __init__(self, start: int, stop: int = None, step: int = 1):
        if stop is None:
            self.start = 0
            self.stop = start
        else:
            self.start = start
            self.stop = stop
        self.step = step

        # Attempt 1:
        # self.start = 0 if stop is None else start
        # self.stop = start if stop is None else stop
        # self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.start >= self.stop:
            raise StopIteration
        value = self.start
        self.start += self.step
        return value


####################################################################################################
# e48: All of the Files
"""
Create a generator function that will take a directory name as an argument. With each iteration, 
the generator should return a single string, representing one line from one file in that 
directory. Thus, if the directory contains five files, and each file contains 10 lines, 
the generator will return a total of 50 strings--each of the lines from file 0, then each of the 
lines from file 1, then each of the lines from file 2, until it gets through all of the lines 
from file 4. If you encounter a file that can’t be opened, it will ignore it and move on.

BTE 1: Modify all_lines such that it doesn’t return a string with each iteration, but rather a 
tuple. The tuple should contain four elements: the name of the file, the current number of the 
file (from all those returned by os.listdir), the line number within the current file, 
and the current line.
"""


def all_lines(path: str) -> Iterable:
    index = 0
    for file in os.listdir(path):
        fp = os.path.join(path, file)
        line_num = 0
        try:
            for line in open(fp):
                yield (
                    file,
                    f"file_index: {index}",
                    f"line_index: {line_num}",
                    line.strip(),
                )
                line_num += 1
        except OSError:
            pass
        finally:
            index += 1


"""
BTE 2: Modify the function such that it returns the first line from each file, and then the 
second line from each file, until all lines from all files are returned. When you finish printing 
lines from shorter files, ignore those files while continuing to display lines from the longer 
files.

Note to self: This one is difficult.  I still don't entirely understand how the implementation is 
working.

BTE 3: Modify all_lines such that it takes two arguments--a directory name, and a string. Only 
those lines containing the string (i.e., for which you can say s in line) should be returned.
"""


def open_file_safely(filename: str) -> List[Iterable]:
    try:
        return open(filename)
    except OSError:
        pass


def parallel_lines(path: str, filter_str: str = None) -> Iterable:
    """Returns the first line from each file, and then the second line from each file, until all
    lines from all files are returned. When you finish printing lines from shorter files,
    ignore those files while continuing to display lines from the longer files"""

    # read all files at once - returns a list of io.TextIOWrappers
    all_files = [
        open_file_safely(os.path.join(path, filename)) for filename in os.listdir(path)
    ]

    # iterate over each file. if file is empty, remove it from all_files
    while all_files:
        for one_file in all_files:
            if one_file is None:
                all_files.remove(one_file)
                continue  # go back to beginning of loop
            one_line = one_file.readline().strip()

            # yield a line of text. if file is exhausted of lines remove file from all_files
            # yield only filter string matches if filter_str is enabled
            if filter_str:
                yield (
                    os.path.basename(one_file.name),
                    one_line,
                ) if one_line and filter_str in one_line else all_files.remove(one_file)
            else:
                yield (
                    os.path.basename(one_file.name),
                    one_line,
                ) if one_line else all_files.remove(one_file)

    # Attempt 1: Doesn't work. Only iterates through files once.
    # file_index = 0
    # for i in range(len(files)):
    #     fp = os.path.join(path, files[i])
    #     with open(fp) as f:
    #         try:
    #             yield f.readline()
    #         except OSError:
    #             pass
    #         finally:
    #             file_index += i
