
- [Basics](#basics)
- [Diagnostic](#diagnostic)
- [Advanced](#advanced)
- [Reference](#reference)

## Basics
The comprehensive example to showcase how decorator works:
```py
from typing import Any
import functools

def basic_decorator(func):
    @functools.wraps(func)  # preserve information about the original function
    # `*args` is needed for positional arguments
    # `**kwargs` is needed for keyword arguments
    def wrapper(*args, **kwargs) -> Any:
        print("Decorating: before...")
        value = func(*args, **kwargs)
        print("Decorating: after.")

        return value

    # note that it returns the function definition other than function call
    return wrapper

def check_in_naive_way(*nums, msg: str = "default") -> int:
    print(f"Function to decorate: {msg}")
    return sum(nums)

@basic_decorator
def check_via_at_symbol(*nums, msg: str = "default") -> int:
    print(f"Function to decorate: {msg}")
    return sum(nums)

check_in_naive_way = basic_decorator(check_in_naive_way)
value = print_in_naive_way(1, 2, 3, msg="simple")
print(f"The sum is {value}")

print("-" * 80)

value = check_via_at_symbol(4, 5, 6, msg="@")
print(f"The sum is {value}")
```

If a built-in function needs to apply customized decorator, it can be done like:
```py
from math import factorial

factorial = basic_decorator(factorial)
print(factorial(10))
```


## Diagnostic
Use code below to check how the function decorated represents. Check what's the difference when `functools` is applied and not.
```py
print(check_via_at_symbol)
print("-" * 80)
print(check_via_at_symbol.__name__)
print("-" * 80)
print(help(check_via_at_symbol))
```

## Advanced
To enable parameters to pass in the decorator function, extra level of wrapping is needed.
```py
from typing import Any
import functools

def advanced_decorator(_func=None, *pos, msg: str = "DEFAULT"):
    """Set up an advanced decorator.

    If `_func` and `*` are not provided, then make sure the decorator is called with `()` even default value is provided for each parameter. Otherwise, such decorator would not work as expected.
    """

    def inner_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            if pos:
                print(f"\tThe positional parameter passed in: {pos}")

            print(f"Message passed in is: {msg}")
            value = func(*args, **kwargs)

            return value

        # note that it returns the function definition other than function call
        return wrapper

    if _func is None:
        return inner_decorator

    return inner_decorator(_func)


@advanced_decorator
def sum_without_calling(*nums) -> int:
    print(f"Get the sum of {nums}")
    return sum(nums)

@advanced_decorator(msg="successful")
def sum_with_calling(*nums) -> int:
    print(f"Get the sum of {nums}")
    return sum(nums)

@advanced_decorator(None, 0, 1, 2)
def sum_with_calling_positional(*nums) -> int:
    print(f"Get the sum of {nums}")
    return sum(nums)


for function in [sum_without_calling, sum_with_calling, sum_with_calling_positional]:
    print("-" * 80)
    value = function(1, 2, 3)
    print(f"{function.__name__!r} {value}")
```


## Reference
- Primer on Python Decorators: https://realpython.com/primer-on-python-decorators/#fancy-decorators
- Python Decorators Examples: https://static.realpython.com/decorators-cheatsheet.pdf
