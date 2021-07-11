
- [Module vs Package](#module-vs-package)
- [Immutable vs Mutable](#immutable-vs-mutable)
- [Module vs Class](#module-vs-class)
- [Class Method vs Static Method](#class-method-vs-static-method)
- [Reference](#reference)


## Module vs Package
- A module is a single `.py` file with Python code
- A package is a hierarchically structured collection of related modules, which is a directory that can contains multiple modules
- An interactive Python shell considers itself as the _main module_

Run `python -m site` to find all location for Python site-packages.


## Immutable vs Mutable
- Immutable objects: tuple, int, float, complex, string, frozen set
- Mutable objects: list, dict, set


## Module vs Class
- Module is a package to encapsulate resuable codes (variable, function, class)
- Class in Python is simillar to Java class, which is structured in a conceptual way

## Class Method vs Static Method

- A class method takes `cls` as first parameter while a static method needs no specific parameters
- A class method can access or modify class state while a static method can’t access or modify it
- Use `@classmethod` decorator in python to create a class method and use `@staticmethod` decorator to create a static method in python
- In general, static methods know nothing about class state. They are utility type methods that take some parameters and work upon those parameters. On the other hand, class methods must have class as parameter.

```py
class Demo:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def instance_method(self):
        print(f"Call instance_method of {self}")

    @classmethod
    def class_method(cls, demo):
        print(f"Call instance_method of {cls}")
        return cls(f"{demo.a!r}1", f"{demo.b}2")

    @staticmethod
    def static_method(cls):
        print("Call static_method")

demo = Demo()
demo.instance_method()
Demo.instance_method(demo)
Demo.class_method()
Demo.static_method()
```


## Reference
- The Meaning of Underscores: https://dbader.org/blog/meaning-of-underscores-in-python
- Python import, sys.path, and PYTHONPATH Tutorial: https://www.devdungeon.com/content/python-import-syspath-and-pythonpath-tutorial
