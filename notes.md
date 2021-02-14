# Python Workout Notes

## Notes on Testing with pytest

### Showing logs like `print` and `logging` in your test

pytest captures stderr by default. To show logs, you need to pass `-o log_cli=true` like below.  
Source: [stackoverflow](https://stackoverflow.com/a/51633600/12207563)

```sh
PYTHONPATH=. pytest -o log_cli=true test/files/test_files.py::test_passwd_to_dict
```

### Using List Comprehensions with `assert`

Using list comprehensions in assertions reference:
https://edricteo.com/list-comprehension-addiction/

```python
import pytest


@pytest.mark.parametrize(
    "inputs, expected",
    [
        (
                ("Chocolate", "Vanilla", "Strawberry"),
                ["Chocolate", "Vanilla", "Strawberry"],
        )
    ],
)
def test_create_scoops_with_different_iterables(inputs, expected):
    assert all([value in expected for value in create_values(inputs)])
```

### Mocks

#### Mocking opening a file

Example of how to mock a file.

```python
def test_final_line():
    mock_open = mock.mock_open(read_data='a\nab\nabc\nabcd')
    with mock.patch("builtins.open", mock_open) as m:
        result = final_line('file_path')
    assert result == 'abcd'


# or 

def test_multi_columns_multi_rows():
    fake_tsv = StringIO('1\n'
                        '1\t2\n'
                        '1\t2\t3\n'
                        '1\t2\t3\t4')
    with mock.patch("builtins.open", return_value=fake_tsv):
        assert sum_multi_columns('file_path') == 32
```

You can also use StringIO

```py
def test_passwd_to_dict():
    fake_passwd = StringIO(
        '###############\n'
        '# User Database\n'
        '###############\n'
        '               \n'
        'nobody:*:-2:-2:Unprivileged User:/var/empty:/usr/bin/false\n'
        'root:*:0:0:System Administrator:/var/root:/bin/sh\n'
        'funnyhaha.org\n'
        'daemon:*:1:1:System Services:/var/root:/usr/bin/false\n')
    with mock.patch("builtins.open", return_value=fake_passwd):
        assert passwd_to_dict('file_path') == {'nobody': '-2', 'root': '0',
                                               'daemon': '1'}
```

### Mock Writing to a File

Reference: https://stackoverflow.com/a/55657594/12207563

```python
import mock
import LogFIle


def test_logfile():
    open_mock = mock.mock_open()
    with mock.patch("builtins.open", open_mock, create=True):
        lf = LogFile('dummy.log')
        lf.write('foobarbaz')
    open_mock.assert_called_with("dummy.log", "w")
    open_mock.return_value.write.assert_called_once_with("foobarbaz")
```

## Lists and Tuples

- Lists are mutable and tuples are immutable, but the real difference between them is how they’re used: lists are for
  sequences of the same type, and tuples are for records that contain different types.
- You can use the built-in sorted function to sort either lists or tuples. You’ll get a list back from your call to
  sorted.
- You can modify the sort order by passing a function to the key parameter. This function will be invoked once for each
  element in the sequence, and the output from the function will be used in ordering the elements.
- If you want to count the number of items contained in a sequence, try using the Counter class from the collections
  module. It not only lets us count things quickly and easily, and provides us with a most_common method, but also
  inherits from dict, giving us all of the dict functionality we know and love.

## Dicts and Sets

- The keys must be hashable, such as a number or string.
- The values can be anything at all, including another dict.
- The keys are unique.
- You can iterate over the keys in a for loop or comprehension.

## Files

- You will typically open files for either reading or writing.
- You can (and should) iterate over files one line at a time, rather than reading the whole thing into memory at once.
- Using `with` when opening a file for writing ensures that the file will be flushed and closed.
- The `csv` module makes it easy to read from and write to CSV files.
- The `json` module’s `dump` and `load` functions allow us to move between Python data structures and JSON-formatted
  strings.

## Functions

> Working with inner functions and closures can be quite surprising and confusing at first. That’s particularly true because our instinct is to believe that when a function returns, its local variables and state all go away. Indeed, that’s normally true--but remember that in Python, an object isn’t released and garbage-collected if there’s at least one reference to it. And if the inner function is still referring to the stack frame in which it was defined, then the outer function will stick around as long as the inner function exists.

## Comprehensions

### List Comprehension vs For loop

On using comprehensions versus `for` loops:
> When you want to transform an iterable into a list, you should use a comprehension. But if you just want to execute something for each element of an iterable, then a traditional for loop is better.

tl;dr - Use comprehension for _tranforming_ values:
> taking values in a list, string, dict, or other iterable and producing a new list based on it--are common in programming. You might need to transform filenames into file objects, or words into their lengths, or usernames into user IDs. In all of these cases, a comprehension is the most Pythonic solution.

Consider what your goal is, and whether you’re better served with a comprehension or a for loop; for example

- Given a string, you want a list of the `ord` values for each character. This should be a list comprehension, because
  you’re creating a list based on a string, which is iterable.
- You have a list of dicts, in which each dict contains your friends’ first and last names, and you want to insert this
  data into a database. In this case, you’ll use a regular `for` loop, because you’re interested in the side effects,
  not the return value.

### Going from list comprehensions to generator expressions:

Generator expressions looks like a list comprehension, but uses parentheses rather than square brackets. We can use a
generator expression in a call to `str.join`, just as we could put in a list comprehension, saving memory in the
process.

```python
# List Comprehension
", ".join([str(num + 1) for num in nums])

# Remove square brackets, becomes generator expression
", ".join(str(num + 1) for num in nums)
```

`map` versus comprehensions
`map` pros: `map` can take multiple iterables in its input and then apply functions that will work with each of them

```python
import operator

letters = 'abcd'
numbers = range(1, 5)

x = map(operator.mul, letters, numbers)
print(' '.join(x))
```

This can be done with a comprehension, but a bit more complex as we need to use `zip` to iterate through two iterables.

```python
import operator

letters = 'abcd'
numbers = range(1, 5)

print(' '.join(operator.mul(one_letter, one_number)
               for one_letter, one_number in zip(letters, numbers)))
```

## Modules

### What’s the difference between a module and a package?

- A __module__ is a single file, with a “.py” suffix. We can load the module using import
- A __package__ is a directory containing one or more Python modules. For example, assume you have the
  modules `first.py`,
  `second.py`, and `third.py`, and want to keep them together. You can put them all into a directory, `mypackage`.
    - Assuming that directory is in sys.path, you can then call:
  ```python
  from mypackage import first
  ```
    - Python will go into the mypackage directory, look for first.py, and import it.

### Importing a package with `__init__.py`

If you import a package wholesale like:

```python
import mypackage
```

__If__ the package directory contains `__init__.py`, importing `mypackage` effectively means that
`__init__.py` is loaded, and thus executed. You can, inside of that file, import one or more of the modules within the
package.

### Creating a Distribution Package

A __distribution package__ is a wrapper around a Python package containing information about the author, compatible
versions, and licensing, as well as automated tests, dependencies, and installation instructions.

- If your distribution package is called `mypackage`, you’ll have a directory called `mypackage`.
- Inside that directory, among other things, will be a subdirectory called `mypackage`, which is where the Python
  package goes.

Creating a distribution package means creating a file called `setup.py`. Here is
a [tutorial](https://packaging.python.org/tutorials/packaging-projects/) from Python docs on how to create a package.

## Objects

### Class vs Instance Attributes

A Python class attribute is an attribute of the class, rather than an attribute of an instance of a class. Python
doesn’t have constants, but we can simulate them with class attributes.

```python
class MyClass(object):
    class_var = 1  # class attribute

    def __init__(self, i_var):
        self.i_var = i_var  # instance attribute
```

Note that all instances of the class have access to `class_var`, and that it can also be accessed as a property of the
class itself:

```python

foo = MyClass(2)
bar = MyClass(3)

foo.class_var, foo.i_var
## 1, 2
bar.class_var, bar.i_var
## 1, 3
MyClass.class_var  ## <— This is key
## 1
```

Reference: [Python Class Attributes: An Overly Thorough Guide](https://www.toptal.com/python/python-class-attributes-an-overly-thorough-guide)

### Inheritance

Example

```python
class Person():
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f'Hello, {self.name}'


class Employee(Person)
    def __init__(self, name, id_number):
        self.name = name
        self.id_number = id_number
```

#### What does `self` do?

- `self` is referring to the current object.
- The first parameter in every class method is `self`
- Any attributes we add to self will stick around after the method returns. And so it’s natural, and thus preferred, to
  assign a bunch of attributes to self in `__init__`.

#### What does `__init__` do?

`__init__` simply adds new attributes to the object.

- Different from `__new__` which is a constructor, which actually creates a new object. Before it creates a new
  instance, it looks for an invokes the `__init__` method.
- Unlike languages such as C# and Java, we don’t just declare attributes in Python; we must actually create and assign
  to them, at runtime, when the new instance is created.

#### Keeping code DRY with `super`

> There’s one weird thing about my implementation of `Employee`, namely that I set self.name in `__init__`. If you’re
> coming from a language like Java, you might be wondering why I have to set it at all, since `Person.__init__` already sets it.
> But that’s just the thing: in Python, `__init__ `really needs to execute for it to set the attribute.
> If we were to remove the setting of `self.name` from `Employee.__init__`, the attribute would never be set.
> By the ICPO rule, only one method would ever be called, and it would be the one that’s closest to the instance.
> Since `Employee.__init__` is closer to the instance than `Person.__init__`, the latter is never called.

Solution: `super` built-in allows us to invoke a method on a parent object without explicitly naming that parent.

```python
class Employee(Person)
    def __init__(self, name, id_number):
        super().__init__(name)
        self.id_number = id_number
```

#### Abstract Base Classes

_Abstract base classes_ are classes that are never instantiated on its own, but various subclasses will inherit.

- In python, you don't need to explicitly declare a class to be abstract.
- However, you _can_ import `ABCMeta` from the [`abc` module](https://docs.python.org/3/library/abc.html).

#### Subclass attribute vs __init__ method

- If there is a default attribute for a subclass that is not going to change, consider just setting it as a subclass
  attribute rather than setting it as an attribute initialized in the `__init__` method in the parent class.
  ```python
  # Parent class
  class Animal:
      def __init__(self, color):
          # Turn the current class object into a string
          self.species: str = self.__class__.__name__
          self.color: str = color

      def __repr__(self):
          return f"{self.color} {self.species}, {self.number_of_legs} legs".lower()

  # Child class - just sets number_of_legs as class attribute rather than setting it as __init__ attribute in parent.
  class Wolf(Animal):
      number_of_legs = 4

      def __init__(self, color):
          super().__init__(color)

  ```

## Limits of OOP principles in Python

> Whether this is right or wrong, (directly accessing data in other objects) is fairly common in the Python
> world. Because all data is public (i.e., there’s no private or protected), it’s considered a good and reasonable thing
> to just scoop the data out of objects. That said, this also means that whoever writes a class has a 
> responsibility to document it, and to keep the API alive--or to document elements that may be deprecated or 
> removed in the future.

> (Unlike Python) In many languages, object-oriented programming is forced on you, such that you’re constantly 
> trying to fit your  programming into its syntax and structure.