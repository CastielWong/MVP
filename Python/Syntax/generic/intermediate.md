
- [Administration](#administration)
- [Memory](#memory)
- [Comprehension](#comprehension)
- [Generator](#generator)
- [Import](#import)
- [Log](#log)
- [Concatenation](#concatenation)
- [Sorting](#sorting)
- [Miscellaneous](#miscellaneous)
- [Profiling](#profiling)
- [Reference](#reference)

## Administration

```py
import platform
import sys

from importlib_metadata import version

print(platform.platform())
print("-" * 80)
print(platform.python_version())
print(sys.version)
print("-" * 80)
print(version("{module}"))
```


## Memory
Check memory with built-in library:
```py
import sys

x = {"a": 1}
print(sys.getsizeof(x))
```

Use a third-party library:
```py
import os

import psutil

process = psutil.Process(os.getpid())
print(process.memory_info())
```


## Comprehension
There are three kinds of comprehensions available: List, Set and Dictionary.

Take List Comprehension for example, which is quite similar to Set and Dictionary, below is the syntax of List Comprehension:
- `new_list = [expression for member in iterable (if condition)]`
- `new_list = [expression (if condition) for member in iterable]`


```py
numbers = [1, -9, 10, 3, -5, 3, 10]

nums_1 = [i for i in numbers if i > 0]
nums_2 = [i if i > 0 else 0 for i in numbers]

comp_set = {i for i in numbers if i > 0}
comp_dict = {i: i * i for i in numbers}

print(nums_1)       # [1, 10, 3, 3, 10]
print(nums_2)       # [1, 0, 10, 3, 0, 3, 10]
print(comp_set)     # {1, 10, 3}
print(comp_dict)    # {1: 1, -9: 81, 10: 100, 3: 9, -5: 25}
```


## Generator
Generator functions are a special kind of function that return a laze iterator. For instance, when open a file, a generator would loop through each line then yields each row, other than read all lines and return as a whole.
```py
# generator function
def csv_reader(file_name):
    for row in open(file_name, "r"):
        yield row

# generator expression
csv_gen = (row for row in open(file_name))
```

When the `yield` statement is hit, the program suspends function execution and returns the yielded value to the caller.
In contrast, return stops function execution completely.
When a function is suspended, the state of that function is saved.
This includes any variable bindings local to the generator, the instruction pointer, the internal stack, and any exception handling.

`next()` is callable for generator object:
```py
def infinite_sequence():
    num = 0
    while True:
        yield num
        num += 1

generator = infinite_sequence()
print(next(generator))
print(next(generator))

nums_list = [num**2 for num in range(5)]
nums_generator = (num**2 for num in range(5))
print(nums_list)        # [0, 1, 4, 9, 16]
print(nums_generator)   # <generator object ...>
```


## Import
Since the checking path for import differs, files in different modules may not be able to see others. Reset `sys.path` is an approach to solve such problem. For the project structure like:
- project
  - package_a
    - module_a.py
    - module_b.py
  - package_b
    - demo.py

The import statements for "demo.py" can be:

```py
import os
import sys

package_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(package_root)

from package import module_a
```

For runtime import, `importlib` can be utilized to locate the customized modules:

```py
import importlib

module_a = importlib.import_module("package.module_a")
```


## Log
```py
import logging

logging.basicConfig(
    format="%(asctime)s %(name)-16s %(levelname)-8s %(message)s", level=logging.INFO
)
logger = logging.getLogger("{logger_name}")
logger.setLevel(logging.INFO)
```


## Concatenation
```py
a = ["a", "b"]
b = [1, 2]

# zip two arrays
for i, j in zip(a, b):
    print(f"{i} - {j}")  # ["a" - 1, "b" - 2]

# get cartesian product
import itertools

alphabet = ["alpha", "beta", "gamma"]
lists = [a, b, alphabet]
for element_tuple in itertools.product(*lists):
    print(element_tuple)  # ("a", 1, "alpha"), ..., ('b', 2, 'gamma')
```


## Sorting
Sort by value in Dictionary:
```py
mapping = {"a": 3, "b": 5, "c": 5, "d": 2}
print(mapping)

# sort the dictionary based on value
sorted_items = sorted(
    mapping.items(), key=lambda item: (-item[1], item[0]), reverse=True,
)
print(sorted_items)  # [('d', 2), ('a', 3), ('c', 5), ('b', 5)]

# convert the array back to dictionary
mapping_sorted = {k: v for k, v in sorted_items}  # {'d': 2, 'a': 3, 'c': 5, 'b': 5}
print(mapping_sorted)
```



## Miscellaneous
```py
# Conversion between chr and int
print(ord("A"))  # 65
print(ord("a"))  # 97
print(ord("2"))  # 50
print(chr(51))  # '3'
print(chr(38))  # '&'

# ---------------------------------------------------------
# String checking
print("a".isalpha())  # True
print("a".isnumeric())  # False
print("1".isalpha())  # False
print("1".isnumeric())  # True
print("a1".isalpha())  # False
print("a1".isnumeric())  # False
print("a1".isalnum())  # True
print("ab".isalpha())  # True
print("12".isnumeric())  # True
# ---------------------------------------------------------
# String generation
import string
import random

strings = random.choices(string.ascii_lowercase + string.digits, k=8)
randomized_string = "".join(strings)
print(f"{randomized_string = }")
# ---------------------------------------------------------
# Type checking
a_set = set()
a_dict = {}

print(isinstance(a_set, set))  # True
print(isinstance(a_dict, dict))  # True

print(type(a_set) is set)  # True
print(type(a_dict) is dict)  # True
# ---------------------------------------------------------
# Function signature
def demo(x=[]):
    print(id(x))
    x.append("a")
    return x

x = []
print(id(x))  # xxxxxx1
# the new list would be passed in
print(demo(x))  # xxxxxx1, ["a"]
print("-----------")
print(demo())  # xxxxxx2, ["a"]
# the list would be the one initiated when `demo()` is called
print(demo())  # xxxxxx2, ["a", "a"]
# ---------------------------------------------------------
# Package checking
import pkg_resources

# check all available packages
package_list = sorted([f"{p.key}=={p.version}" for p in pkg_resources.working_set])
print(package_list)
# ---------------------------------------------------------
# Module reload
from importlib import reload

reload({module})
# ---------------------------------------------------------
# Create a class which can be sliced
class SliceMaker(object):
    def __getitem__(self, item):
        return item

s = SliceMaker()
print(s[2])
print(s[1:5])
```


## Profiling
Below is a sample to profile different approaches to check out the performance difference:
```py
import random
import timeit

TAX_RATE = .7
txns = [random.randrange(100) for _ in range(100_000)]

def get_price(txn):
    return txn * (1 + TAX_RATE)

def get_prices_with_map():
    return list(map(get_price, txns))

def get_prices_with_comprehension():
    return [get_price(txn) for txn in txns]

def get_prices_with_loop():
    prices = []
    for txn in txns:
        prices.append(
            get_price(txn)
        )
    return prices

# time cost: map < comprehension < loop
print(timeit.timeit(get_prices_with_map, number=100))
print(timeit.timeit(get_prices_with_comprehension, number=100))
print(timeit.timeit(get_prices_with_loop, number=100))
```


## Reference
- When to Use a List Comprehension in Python: https://realpython.com/list-comprehension-python/
- How to Use Generators and yield in Python: https://realpython.com/introduction-to-python-generators/
- Usage of slots: https://stackoverflow.com/questions/472000/usage-of-slots
