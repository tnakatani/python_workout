# Python Workout Notes

## Notes on Testing with pytest

### Showing logs like `print` and `logging` in your test

pytest captures stderr by default. To show logs, you need to pass `-o log_cli=true` like below.  
Source: [stackoverflow](https://stackoverflow.com/a/51633600/12207563)

```sh
PYTHONPATH=. pytest -o log_cli=true test/files/test_files.py::test_passwd_to_dict
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
  data into a database. In this case, you’ll use a regular `for` loop, because you’re interested in the side effects, not
  the return value.

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

