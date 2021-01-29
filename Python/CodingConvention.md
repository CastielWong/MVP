
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
| Function | Snake Case | demo_function |
| Constant | Macro Case | GLOBAL_CONSTANT |
| Variable | Snake Case | class_var |
| Parameter | Snake Case | function_param |

Note that even though Python doesn't support private element like normal OOP language like JAVA, it's highly recommended to add a leading "_" to any private element (function/variable) for clarification.


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


## Docstring

Apply triple quotes for Docstring.

```py
def demo_function(arg1: str) -> None:
    """
    """
```


## Reference

- Code Review Developer Guide: https://google.github.io/eng-practices/review/
- Naming Convetion: https://en.wikipedia.org/wiki/Naming_convention_(programming)
- The Meaning of Underscores: https://dbader.org/blog/meaning-of-underscores-in-python
