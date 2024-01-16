
- [Anatomy](#anatomy)
- [Constructor](#constructor)
- [Property](#property)
- [Interface](#interface)
  - [Informal](#informal)
    - [Metaclass](#metaclass)
    - [Virtual Base](#virtual-base)
  - [Formal](#formal)
- [Reference](#reference)

Even though Python was not designed for Object-Oriented Programming at the very beginning, it provides more and more features to support OOP.


## Anatomy
```py
class Demo:
    # # specify attributes needed to for memory saving
    # # if it's enabled, then `__slots__` will be accessible instead of `__dict__`
    # __slots__ = ["a", "b", "c"]

    def __init__(self, a: str, b: int):
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
        return f"<{self.__class__.__name__}(\"{self.a}\", {self.b})>"


demo = Demo()
print(str(demo))    # This is demo
print(repr(demo))   # <Demo("1", 2)>
print(demo)         # This is demo

print(vars(demo))       # {'a': '1', 'b': 2, 'c': 3}
# object anatomy
print(dir(demo))        # [..., 'add_c']

# class anatomy
print(dir(Demo))        # [..., 'a', 'add_c', 'b', 'c']

# class lineage --- Method Resolution Order
print(Demo.__mro__)     # (<class 'Demo'>, <class 'object'>)
```

## Constructor
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

    # convert the dict to key-value pair for instantiation
    role = Role(**data)
```

## Property
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

It turns out that some of the attributes would be corrupted.
So Python introduces Property decorator to take care Getter, Setter and Deleter for attributes.

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

## Interface
There are two types of Interface implementation Python provides.
One is formal Interface, while the other is informal Interface.

The informal Interface can be quite confusing, it's suggested to implement formal Interface whenever possible.

### Informal
Informal Interface doesn't guarantee the implementation of each method inside the interface.

For the example code below, though both `Achiever` and `Partaker` both inherit(implement) `InfromalInterface`, `Partaker` doesn't implement all methods required.
For that reason, we don't expect `Partaker` is a subclass of `InformalInterface` theoretically.
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

#### Metaclass
Metaclass can solve problem mentioned before, yet it introduces two other inconsistency problems:
- method parameter is neglected as long as function name is matched
- there is no explicit inheritance defined in Method Resolution Order

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

#### Virtual Base
The Virtual base class is to provide the interface hierarchy for clarity.
However, it makes the hierarchy more complicated to understand.
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


### Formal
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

Even though there is no compiled error when defining `Partaker`, error will be thrown when it's about to instantiate.


## Reference
- Implementing an Interface in Python: https://realpython.com/python-interface/
- Python Metaclasses: https://realpython.com/python-metaclasses/
