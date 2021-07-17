
- [Memory](#memory)
- [Generator](#generator)
- [Import](#import)
- [Log](#log)
- [Concatenation](#concatenation)
- [Sorting](#sorting)
- [Object-Oriented Programming](#object-oriented-programming)
  - [Anatomy](#anatomy)
  - [Constructor](#constructor)
  - [Property](#property)
  - [Interface](#interface)
    - [Informal](#informal)
      - [Metaclass](#metaclass)
      - [Virtual Base](#virtual-base)
    - [Formal](#formal)
- [Miscellaneous](#miscellaneous)
- [Reference](#reference)


## Memory
Check memory with built-in library:
```py
import sys

x = {"a": 1}
print(sys.getsizeof(x))
```

Use a third-party library:
```py
import os, psutil

process = psutil.Process(os.getpid())
print(process.memory_info())
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

When the `yield` statement is hit, the program suspends function execution and returns the yielded value to the caller. In contrast, return stops function execution completely. When a function is suspended, the state of that function is saved. This includes any variable bindings local to the generator, the instruction pointer, the internal stack, and any exception handling.

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
  - packagea
    - module_a.py
    - module_b.py
  - packageb
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


## Object-Oriented Programming
### Anatomy
```py
class Demo:
    # # specify attributes needed to for memory saving
    # # if it's enabled, then `__slots__` will be accessible instead of `__dict__`
    # __slots__ = ["a", "b", "c"]

    def __init__(self):
        self.a = "1"
        self.b = 2
        self.add_c()

    def add_c(self):
        self.c = 3

    def __str__(self):
        return "This is demo"

    # it would be called via print() if there is no __str__()
    # or it would be called if the object is inside the list to print
    def __repr__(self):
        return f"<Demo(\"{self.a}\", {self.b})>"


demo = Demo()
print(demo.__str__())   # This is demo
print(demo.__repr__())  # <Demo("1", 2)>
print(demo)             # This is demo

print(vars(demo))       # {'a': '1', 'b': 2, 'c': 3}
# object anatomy
print(dir(demo))        # [..., 'add_c']

# class anatomy
print(dir(Demo))        # [..., 'a', 'add_c', 'b', 'c']

# class lineage --- Method Resolution Order
print(Demo.__mro__)     # (<class 'Demo'>, <class 'object'>)
```

### Constructor
```py
class Role:
    def __init__(self, **data):
        self.id = data["id"]
        self.name = data["name"]

if __name__ == "__main__":
    data = {
        "id": 1,
        "name": "admin"
    }

    # need to convert the dict to key-value pair first
    role = Role(**data)
```

### Property
A general way to access attributes:
```py
class Employee:
    """
    Create docstring...
    """

    def __init__(self, first, last):
        """
        Sample docstring for constructor.
        """
        self.first = first
        self.last = last
        self.email = f"{first}.{last}@email.com"

    def fullname(self):
        """
        Sample docstring for fullname().
        """
        return f"{self.first} {self.last}"


# output the class docstring only
print(Employee.__doc__)
# output the docstring for the whole class
print(help(Employee))

emp = Employee("John", "Doe")
emp.first = "Jane"
print(emp.first)        # Jane
print(emp.email)        # John.Doe@email.com
print(emp.fullname())   # Jane Doe
```

It turns out that some of the attributes would be corrupted. So Python introduce Property decorator to take care Getter, Setter and Deleter for attributes.

```py
class Employee:
    def __init__(self, first, last, age=-1):
        self._first = first
        self._last = last
        self._age = age

    @property
    def email(self):
        return f"{self._first}.{self._last}@email.com"

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age):
        self._age = age

    @property
    def fullname(self):
        return f"{self._first} {self._last}"

    @fullname.setter
    def fullname(self, name):
        first, last = name.split(" ")
        self._first = first
        self._last = last

    @fullname.deleter
    def fullname(self):
        print("DELETING...")
        self._first = None
        self._last = None
        self._age = -1

emp = Employee("John", "Doe", 30)
emp.first = "Jane"
print(emp.first)        # Jane
print(emp.email)        # Jane.Doe@email.com
print(emp.fullname)     # Jane Doe

print(emp.age)          # 30
emp.age = 40
print(emp.age)          # 40

emp.fullname = "Charlie Smith"
print(emp.fullname)     # Charlie Smith
del emp.fullname        # DELETING...
```

### Interface
There are two types of Interface implementation Python provides. One is Formal Interface, while the other is Informal Interface.

The Informal Interface can be quite confusing, it's suggested to implement Formal Interface whenever possible.

#### Informal
Informal Interface doesn't guarantee the implementation of each method inside the interface.

For the example code below, though both `Achiever` and `Partaker` both inherit(implement) `InfromalInterface`, `Partker` doesn't implement all methods required. For that reason, we don't expect `Partaker` is a subclass of `InformalInterface` theoretically.
```py
class InformalInterface:
    def load_data_source(self, path: str, file_name: str) -> str:
        pass

    def extract_text(self, full_file_name: str) -> dict:
        pass

class Achiever(InformalInterface):
    def load_data_source(self, path: str, file_name: str) -> str:
        pass

    def extract_text(self, full_file_name: str) -> dict:
        pass

class Partaker(InformalInterface):
    def load_data_source(self, path: str, file_name: str) -> str:
        pass

    def extract_text_from_email(self, full_file_name: str) -> dict:
        pass

print(issubclass(Achiever, InformalInterface))  # True
print(issubclass(Partaker, InformalInterface))  # True

print(Achiever.__mro__) # Achiever, InformalInterface, object
print(Partaker.__mro__) # Partaker, InformalInterface, object

print(Achiever())       # an Achiever object
print(Partaker())       # an Partaker object
```

##### Metaclass
Metaclass can solve problem mentioned beofre, yet it introduces two other inconsistency problems:
- method parameter is neglected as long as function name is matched
- there is no explict inheritance defined in Method Resolution Order

```py
class CustomMeta(type):
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, "load_data_source")
            and callable(subclass.load_data_source)
            and hasattr(subclass, "extract_text")
            and callable(subclass.extract_text)
        )

class Interface(metaclass=CustomMeta):
    pass

class Achiever:
    def load_data_source(self, file_name: str) -> str:
        pass

    def extract_text(self, full_file_name: str) -> dict:
        pass

class Partaker:
    def load_data_source(self, path: str, file_name: str) -> str:
        pass

    def extract_text_from_email(self, full_file_name: str) -> dict:
        pass

print(issubclass(Achiever, Interface))  # True
print(issubclass(Partaker, Interface))  # False

print(Achiever.__mro__) # Achiever, object
print(Partaker.__mro__) # Partaker, object
```

##### Virtual Base
The virutal base class is to provide the interface hierarchy for clarity. However, it makes the hierarchy more complicated to understand.
```py
class CustomMeta(type):
    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        return (
            hasattr(subclass, "load_data_source")
            and callable(subclass.load_data_source)
            and hasattr(subclass, "extract_text")
            and callable(subclass.extract_text)
        )

class Interface(metaclass=CustomMeta):
    pass

class InterfaceSuper:
    def load_data_source(self, path: str, file_name: str) -> str:
        pass

    def extract_text(self, full_file_name: str) -> dict:
        pass

class Achiever(InterfaceSuper):
    pass

class Partaker:
    def load_data_source(self, path: str, file_name: str) -> str:
        pass

    def extract_text(self, full_file_name: str) -> dict:
        pass

print(issubclass(Achiever, Interface))  # True
print(issubclass(Partaker, Interface))  # True

print(Achiever.__mro__) # Achiever, InterfaceSuper, object
print(Partaker.__mro__) # Partaker, object
```


#### Formal
In order to create a formal Python interface, a few more tools from Python’s `abc` module are needed.
```py
import abc

class FormalInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "load_data_source")
            and callable(subclass.load_data_source)
            and hasattr(subclass, "extract_text")
            and callable(subclass.extract_text)
        )

    @abc.abstractmethod
    def load_data_source(self, path: str, file_name: str):
        raise NotImplementedError

    @abc.abstractmethod
    def extract_text(self, full_file_path: str):
        raise NotImplementedError

class Achiever(FormalInterface):
    def load_data_source(self, path: str, file_name: str) -> str:
        pass

    def extract_text(self, full_file_name: str) -> dict:
        pass

class Partaker(FormalInterface):
    def load_data_source(self, path: str, file_name: str) -> str:
        pass

    def extract_text_from_email(self, full_file_name: str) -> dict:
        pass

print(issubclass(Achiever, FormalInterface))  # True
print(issubclass(Partaker, FormalInterface))  # True

print(Achiever.__mro__) # Achiever, FormalInterface, object
print(Partaker.__mro__) # Partaker, FormalInterface, object

print(Achiever())       # an Achiever object
print(Partaker())       # TypeError thrown
```

Even though there is no compiled error when defining `Partker`, error will be thrown when it's about to instantiated.



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
```


## Reference
- How to Use Generators and yield in Python: https://realpython.com/introduction-to-python-generators/
- Usage of slots: https://stackoverflow.com/questions/472000/usage-of-slots
- Implementing an Interface in Python: https://realpython.com/python-interface/
