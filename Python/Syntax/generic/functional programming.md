
- [Map](#map)
- [Filter](#filter)
- [Reduce](#reduce)
- [Lambda](#lambda)
- [Reference](#reference)


## Map
Syntax: `map(function, iterable[, iterable1, iterable2, ...., iterableN])`

Straightforward example:
```py
iter_1 = [1, 2, 3]
iter_2 = [4, 5, 6, 7]
iter_3 = [8, 9]

power = map(pow, iter_1, iter_2)
print(list(power))  # [1, 32, 729]

sumer = map(lambda x, y, z: x + y + z, iter_1, iter_2, iter_3)
print(list(sumer))  # [13, 16]
```

Instead of concatenate element from each iterator for the function, `startmap` passes each tuple as the input:
```py
from itertools import starmap

tuple_1 = (2, 5)
tuple_2 = (3, 6)

power = starmap(pow, [tuple_1, tuple_2])
print(list(power))      # [32, 729]
```

Replace `map()` with list comprehension and generator expression:
```py
def square(number):
    return number ** 2

numbers = [1, 2, 3]

map_obj = map(square, numbers)
print(list(map_obj))                # [1, 4, 9]

list_comprehension = [square(x) for x in numbers]
print(list_comprehension)           # [1, 4, 9]

generator_expression = (square(x) for x in numbers)
print(list(generator_expression))   # [1, 4, 9]
```


## Filter
Syntax: `filter(function, iterable)`

Straightforward example:
```py
def is_positive(n):
    return n > 0

numbers = [-2, -1, 0, 1, 2]

# [1, 2]
print(list(filter(is_positive, numbers)))
print(list(filter(lambda n: n > 0, numbers)))
```

Other than filter the true values out then do the reversion, `filterfalse()` provides the opposite way to achieve the purpose:
```py
from itertools import filterfalse

def is_even(number):
    return number % 2 == 0

numbers = [1, 3, 10, 45, 6, 50]

print(list(filterfalse(is_even, numbers)))  # [1, 3, 45]
```

Replace `filter()` with list comprehension and generator expression:
```py
def is_even(number):
    return number % 2 == 0

numbers = [1, 3, 10, 45, 6, 50]

filter_obj = filter(is_even, numbers)
print(list(filter_obj))             # [10, 6, 50]

list_comprehension = [x for x in numbers if is_even(x)]
print(list_comprehension)           # [10, 6, 50]

generator_expression = (x for x in numbers if is_even(x))
print(list(generator_expression))   # [10, 6, 50]
```


## Reduce
Syntax: `reduce(function, iterable[, initializer])`

Rough equivalent implementation of `reduce()`:
```py
def reduce(function, iterable, initializer=None):
    it = iter(iterable)
    if initializer is None:
        value = next(it)
    else:
        value = initializer

    for element in it:
        value = function(value, element)
    return value
```

Straightforward example:
```py
from functools import reduce
import math
import operator

def cus_prod(a, b):
    return a * b

numbers = [1, 2, 3, 4]

print(reduce(cus_prod, numbers))            # 24
print(reduce(lambda a, b: a * b, numbers))  # 24
print(reduce(operator.mul, numbers))        # 24
print(math.prod(numbers))                   # 24
```

Though `reduce()` combines elements to produce a single result, that result can be a composite object like a list or a tuple. For that reason, it's a very generalized Higher-Order Function from which many other functions can be implemented. Like to implement `map()` and `filter()`:
```py
from functools import reduce

def custom_map(func, iterable):
    return reduce(
        lambda items, value: items + [func(value)],
        iterable,
        []
    )

def custom_filter(func, iterable):
    return reduce(
        lambda items, value: items + [value] if func(value) else items,
        iterable,
        []
    )

numbers = [1, 2, 3, 4, 5]

# ['1', '2', '3', '4', '5']
print(list(map(str, numbers)))
print(list(custom_map(str, numbers)))

# [2, 4]
print(list(filter(lambda x: x % 2 == 0, numbers)))
print(list(custom_filter(lambda x: x % 2 == 0, numbers)))
```



## Lambda
In Python, a Lambda Calculus consists of:
- keyword: `lambda`
- bound variable: input, which is the argument to the lambda function
- body: output, the return value(s)

```py
def func_add(x, y):
    return x + y

lambda_add = lambda x, y: x + y

print(func_add_one(2, 1))
print(lambda_add_one(2, 1))
```

Use as high order function:
```py
high_ord_func = lambda x, func: x + func(x)

print(high_ord_func(2, lambda x: x * x))    # 6

print(high_ord_func(2, lambda x: x + 3))    # 7
```

```py
# x is passed as an argument to outer_func()
# y is a variable local to outer_func()
# z is an argument passed to inner_func()
def outer_func(x):
    y = 4
    def inner_func(z):
        print(f"{x = }, {y = }, {z = }")
        return x + y + z

    return inner_func

def outer_func_lambda(x):
    y = 4
    return lambda z: x + y + z

for i in range(3):
    closure = outer_func(i)
    # closure = outer_func_lambda(i)
    print(f"closure({i+5}) = {closure(i+5)}")
```


```py
from functools import reduce

animals = ["cat", "dog", "cow"]

obj_map = map(lambda x: x.upper(), animals)
obj_filter = filter(lambda x: "o" in x, animals)
obj_reduce = reduce(lambda acc, x: f"{acc} | {x}", animals)

print(obj_map)
print([x.upper() for x in animals])

print(obj_filter)
print([x for x in animals if "o" in x ])

print(obj_reduce)
print("|".join([x for x in animals]))
```



## Reference
- Python's map() - Processing Iterables Without a Loop: https://realpython.com/python-map-function/
- Python's filter() - Extract Values From Iterables: https://realpython.com/python-filter-function/
- Python's reduce() - From Functional to Pythonic Style: https://realpython.com/python-reduce-function/
- How to Use Python Lambda Functions: https://realpython.com/python-lambda/
- Functional Programming in Python: https://realpython.com/python-functional-programming/
