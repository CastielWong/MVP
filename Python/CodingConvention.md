
This documentation is to suggest/recommend the good coding style in Python.

- [General](#general)
- [Naming Convention](#naming-convention)
- [Header](#header)
- [Importing](#importing)
- [Type Hinting](#type-hinting)
- [Docstring](#docstring)
- [Docker](#docker)
- [Reference](#reference)


## General

| Item | Detail |
| --- | --- |
| Indentation | 4 spaces, no tab |
| Blank Lines | 2 for top-level definitions, like between import statements and the first class/function definition |
| Blank Lines | 1 between method defintions |
| Blank Lines | 1 when it improves code readability |
| Type Hinting | Apply Type Hinting whenever defining a new function |


## Naming Convention

| Type | Pattern | Example |
| --- | --- | --- |
| Package | Snake Case | package_a |
| Module | Snake Case | module_a |
| Class | Pascal Case | DemoClass |
| Function | Snake Case | demo_function() |
| Constant | Macro Case | GLOBAL_CONSTANT |
| Variable | Snake Case | class_var |
| Parameter | Snake Case | function_param |

Note that even though Python doesn't support private element like normal OOP language like JAVA, it's highly recommended to add a leading "_" to any private element (function/variable) for clarification.


## Header

It's a good practice to put clarified header at the top of each python file. For instance:

```py
#!/usr/bin/env python
# -*- coding: utf-8 -*-
```


## Importing

There are three levels imports: in-built, third-party, customized. For better readability, it's suggested to have the import statements to follow order as the example:

```py
import {in-built}

import {third-party}

import {customized}
```

And there are three kinds of import statements, it's suggested to import them like:

```py
import {package}
import {package} as {pac}
from {package} import {module}
```

Import statements under the same style are ordered alphabetically for sure.


## Type Hinting

It improves readability to have function annotation clarified as [PEP 484](https://www.python.org/dev/peps/pep-0484/) indicated. Below is examples for common use cases:

```py
def demo_main() -> None:
    pass

def demo_func_a(arg1: str, arg2: dict) -> list:
    pass

def demo_func_b(arg: [list, dict]) -> int:
    pass
```


## Docstring

Use triple quotes and apply [Google Style](https://google.github.io/styleguide/pyguide.html) for Docstring.

```py
def demo_function(arg1: int, arg2: float) -> [str, int]:
    """
    This is a demo function.

    Args:
        arg1: argument 1
        arg2: argument 2

    Returns:
        An answer in string or interger
    """
    pass
```

## Docker

For docker-compose, the configuration order structure is suggested to be:
- config related to container
- config for network
- config for volume
- config about orchestration

For instance,
```yaml
version: 3.5

volumes:
  vol_check_var:
    name: lab_xxx

services:
  xxx:
    restart: always
    container_name: ...
    image: ...
    environments:
      - ...=...
    command:
      - ...
    networks:
      - lab_xxx
    ports:
      - ...:...
    volumes:
      - vol_check_var:/opt/xxx/var
    depends_on:
      - ...

networks:
  lab_xxx:
    name: ...
    driver: bridge
    ipam:
      cofing:
        - subnet: a.b.c.d/..
```


## Reference

- Code Review Developer Guide: https://google.github.io/eng-practices/review/
- Naming Convetion: https://en.wikipedia.org/wiki/Naming_convention_(programming)
- The Meaning of Underscores: https://dbader.org/blog/meaning-of-underscores-in-python
