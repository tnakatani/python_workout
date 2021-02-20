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
import collections
import os
import time
from typing import Generator, Iterable, TextIO


class MyEnumerate:
    def __init__(self, data):
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
        yield index, data[index]
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


class Circle2:
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


class CircleInherit(Circle2):
    def __init__(self, data, end: int = 0):
        super().__init__(data, end)
        self.returns = "data"


"""
BTE 2: Implement Circle as a generator function, rather than as a class.
"""


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
            self.stop = start
            self.start = 0
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


def all_lines(path: str) -> Generator:
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


def open_file_safely(filename: str) -> TextIO:
    try:
        return open(filename)
    except OSError:
        pass


def parallel_lines(path: str, filter_str: str = None) -> Generator:
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


####################################################################################################
# e49: Elapsed Since

"""
Write a generator function whose argument must be iterable. With each iteration, the generator 
will return a two-element tuple. The first element in the tuple will be an integer indicating how 
many seconds have passed since the previous iteration. The tuple’s second element will be the 
next item from the passed argument.You can use time.perf_counter, which returns the number of 
seconds since the program was started. 

BTE 1: Add an argument for the minimum amount of time that must elapse between iterations. If the 
next element is requested via the iterator protocol (i.e., next), and the time elapsed since the 
previous iteration is greater than the user-defined minimum, then the value is returned. If not, 
then the generator uses time.sleep to wait until the appropriate amount of time has elapsed.
"""


def elapsed_since(data: Iterable, min_wait: int = 0):
    """A generator that takes an iterable as input. With each iteration, it yields a tuple
    containing the time since the previous iteration and the data.

    If the next element is requested via the iterator protocol (i.e., next), and the time elapsed
    since the previous iteration is greater than the user-defined minimum, then the value is
    returned.
    """
    last_time = None  # Must be None for or logic to work below since 0 is True
    for i in data:
        current_time = time.perf_counter()
        delta = current_time - (last_time or current_time)
        if delta < min_wait:
            delta = min_wait - delta
            time.sleep(delta)
        last_time = time.perf_counter()
        yield delta, i

    # Attempt 1: Works
    # last_time = None  # Must be None for or logic to work below since 0 is True
    # for i in data:
    #     current_time = time.perf_counter()
    #     delta = current_time - (last_time or current_time)
    #     last_time = time.perf_counter()
    #     if delta < min_elapsed:
    #         new_elapsed = min_elapsed - delta
    #         time.sleep(new_elapsed)
    #         yield new_elapsed, i
    #     else:
    #         yield delta, i


"""
BTE 2: Write a generator function, file_usage_timing, that takes a single directory name as an 
argument. With each iteration, we get a tuple containing not just the current filename, but also 
the three reports that we can get about a file’s most recent usage: its access time (atime), 
modification time (mtime), and creation time (ctime). Hint: all are available via the os.stat 
function.
"""


def file_usage_timing(path: str) -> Generator:
    for file in os.listdir(path):
        info = os.stat(os.path.join(path, file))
        yield file, info.st_atime, info.st_mtime, info.st_ctime


"""
BTE 3: Write a generator function that takes two elements: an iterable and a function. With each 
iteration, the function is invoked on the current element. If the result is True, then the 
element is returned as is. Otherwise, the next element is tested, until the function returns 
True. Alternative: implement this as a regular function that returns a generator expression.
"""


def yield_filter(data: Iterable):
    for i in data:
        if bytes(i, "utf-8"):
            yield i


####################################################################################################
# e50: MyChain

"""
Implement a generator function called mychain that emulates itertool's chain method. It takes any 
number of arguments, each of which is an iterable.  With each iteration, it should return the next 
element from the current iterable, or the first element from the subsequent iterable--unless 
you’re at the end, in which case it should exit.
"""


def mychain(*args):
    for arg in args:
        for item in arg:
            yield item


"""
BTE 1: The built-in zip function returns an iterator that, given iterable arguments, 
returns tuples taken from those arguments’ elements. The first iteration will return a tuple from 
the arguments’ index 0, the second iteration will return a tuple from the arguments’ index 1, 
and so on, stopping when the shortest of the arguments ends. Thus zip('abc', [10, 20, 
30]) returns the iterator equivalent of [('a', 10), ('b', 20), ('c', 30)]. Write a generator 

function that reimplements zip in this way.
"""


class MyZip:
    @staticmethod
    def is_mapping(obj: Iterable) -> bool:
        # https://docs.python.org/3/glossary.html#term-mapping
        return isinstance(obj, collections.abc.Mapping)

    def zip(self, *args) -> tuple:
        """Implementation of zip().  For dicts, returns the dictionary keys"""
        # get the shortest length among iterables
        min_arg_length = len(min(args, key=len))
        for i in range(min_arg_length):
            output = []
            for arg in args:
                # check if object is a dictionary
                if self.is_mapping(arg):
                    keys = list(arg.keys())
                    output.append(keys[i])
                    continue
                output.append(arg[i])
            yield tuple(o for o in output)

    # Native python version for comparison
    @staticmethod
    def python_zip(*iterables):
        """Native Python's implementation of zip"""
        # zip('ABCD', 'xy') --> Ax By
        sentinel = object()
        iterators = [iter(it) for it in iterables]
        while iterators:
            result = []
            for it in iterators:
                elem = next(it, sentinel)
                if elem is sentinel:
                    return
                result.append(elem)
            yield tuple(result)

    # Attempt 1: Doesn't work
    # while min_length:
    #     output = []
    #     for arg in args:
    #         print(arg)
    #         output.append(arg[counter])
    #     min_length -= 1
    #     yield output


"""
BTE 2: Reimplement the all_lines function from exercise 49 using mychain.
"""


def all_lines_mychain(path: str) -> Generator:
    files = (
        open(os.path.join(path, file))
        for file in os.listdir(path)
        if os.path.isfile(os.path.join(path, file))
    )
    return mychain(*files)

    # Attempt 1: Works
    # files = []
    # for file in os.listdir(path):
    #     try:
    #         files.append(open(os.path.join(path, file)))
    #     except OSError:
    #         pass
    # return mychain(*files)

    # Book solution
    # return mychain(*(open(os.path.join(path, filename))
    #                  for filename in os.listdir(path)
    #                  if os.path.isfile(os.path.join(path, filename))))


"""
BTE 3: In the “Beyond the exercise” section for exercise 48, you implemented a MyRange class, 
which mimics the built-in range class. Now do the same thing, but using a generator expression.
"""

def myrange_generator(start: int, stop: int = None, step: int = 1) -> Generator:
    if stop is None:
        stop = start
        start = 0
    else:
        start = start
        stop = stop

    while start < stop:
        value = start
        start += step
        yield value

# Book solution
# def myrange(first, second=None, step=1):
#     if second is None:
#         current = 0
#         stop = first
#
#     else:
#         current = first
#         stop = second
#
#     while current < stop:
#         yield current
#         current += step