
- [Module vs Package](#module-vs-package)
- [Immutable vs Mutable](#immutable-vs-mutable)
- [Module vs Class](#module-vs-class)
- [Method Types](#method-types)
- [Late Binding](#late-binding)
- [Reference](#reference)


> Because Python applications are typically distributed as source code, the role of the Python runtime is to convert the Python source code and execute it in one step. Internally, the CPython runtime does compile your code. A popular misconception is that Python is an interpreted language. It is actually compiled.

## Module vs Package
- A module is a single `.py` file with Python code
- A package is a hierarchically structured collection of related modules, which is a directory that can contains multiple modules
- A package is just a module with two defined attributes (`__package` and `__path__`)
- An interactive Python shell considers itself as the _main module_

Run `python -m site` to find all location for Python site-packages.


## Immutable vs Mutable
- Immutable objects: tuple, int, float, complex, string, frozen set
- Mutable objects: list, dict, set


## Module vs Class
- Module is a package to encapsulate resuable codes (variable, function, class)
- Class in Python is simillar to Java class, which is structured in a conceptual way

## Method Types
Class Method vs Static Method:
- A class method takes `cls` as first parameter while a static method needs no specific parameters
- A class method can access or modify class state while a static method can’t access or modify it
- Use `@classmethod` decorator in python to create a class method and use `@staticmethod` decorator to create a static method in python
- In general, static methods know nothing about class state. They are utility type methods that take some parameters and work upon those parameters. On the other hand, class methods must have class as parameter.

```py
class Demo:
    def __init__(self, a="0", b="0"):
        self.a = a
        self.b = b

    def __str__(self):
        return f"({self.a}, {self.b})"

    def instance_method(self):
        print(f"Instance Method: {self}")

    @classmethod
    def class_method(cls, demo):
        obj_new = cls(f"{demo.a!r}1", f"{demo.b}2")
        print(f"Call Method: {obj_new}")
        return obj_new

    @staticmethod
    def static_method():
        print("Static Method")


obj_1 = Demo()

obj_1.instance_method()             # Instance Method: (0, 0)
Demo.instance_method(obj_1)         # Instance Method: (0, 0)

obj_2 = obj_1.class_method(obj_1)   # Call Method: ('0'1, 02)
obj_3 = Demo.class_method(obj_1)    # Call Method: ('0'1, 02)
obj_2.instance_method()             # Instance Method: ('0'1, 02)
print(str(obj_2) == str(obj_3))     # True
print(obj_2 is obj_3)               # False

obj_1.static_method()               # Static Method
```

Though `classmethod` and `staticmethod` works quite similar, one of the biggest difference between them is that `staticmethod` would still return attributes superclass has when there is difference in subclasses.
```py
class Parent:
    count = 0

    @classmethod
    def get_count_class(cls):
        return cls.count

    @staticmethod
    def get_count_static():
        return Parent.count


class Child(Parent):
    count = 1


p = Parent()
print(p.get_count_class())  # 0
print(p.get_count_static()) # 0

c = Child()
print(c.get_count_class())  # 1
print(c.get_count_static()) # 0
```


## Late Binding
Python’s closures are late binding. This means that the values of variables used in closures are looked up at the time the inner function is called.

Whenever any of the returned functions are called, the value `i` in the loop is looked up in the surrounding scope at call time. By then, the loop has completed and `i` is left with its final value.

Below shows the side effect of Late Binding:
```py
# ordinary function
def multipliers():
    multipliers = []

    for i in range(5):
        def multiplier(x):
            return i * x
        multipliers.append(multiplier)

    return multipliers

# lambda
def multipliers_lambda():
    return [lambda x : i * x for i in range(5)]

# both are [8, 8, 8, 8, 8]
print([m(2) for m in multipliers()])
print([m(2) for m in multipliers_lambda()])
```

To fix the side-effect:
```py
# ordinary function
def multipliers():
    multipliers = []

    for i in range(5):
        def multiplier(x, i=i):
            return i * x

        multipliers.append(multiplier)

    return multipliers
# lambda
def multipliers_lambda():
    return [lambda x, i=i : i * x for i in range(5)]

# both are [0, 2, 4, 6, 8]
print([m(2) for m in multipliers()])
print([m(2) for m in multipliers_lambda()])
```


## Reference
- Guide to the CPython Source Code: https://realpython.com/cpython-source-code-guide/
- The Meaning of Underscores: https://dbader.org/blog/meaning-of-underscores-in-python
- Python import, sys.path, and PYTHONPATH Tutorial: https://www.devdungeon.com/content/python-import-syspath-and-pythonpath-tutorial
- Late Binding Closures: https://docs.python-guide.org/writing/gotchas/#late-binding-closures
- Python's Instance, Class, and Static Methods Demystified: https://realpython.com/instance-class-and-static-methods-demystified/
