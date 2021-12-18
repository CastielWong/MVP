
- [Basics](#basics)
- [Diagnostic](#diagnostic)
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
def check_via_at_symbol(*nums, msg: str = "default") -> str:
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


## Reference
- Primer on Python Decorators: https://realpython.com/primer-on-python-decorators/#fancy-decorators
