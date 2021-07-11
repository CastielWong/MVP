
- [Module](#module)
  - [Definition](#definition)
  - [Execution](#execution)
  - [Cache](#cache)
- [Package](#package)
- [Reference](#reference)


## Module
Any python source file is considered as a __module__. What happens insidea mudule, stays in a module.

If a file isn't on the `sys.path`, it won't be able to import.

### Definition
Below is the content of a python file named "spam.py":
```py
def grok(x):
    pass

def blah(x):
    pass
```

To execute and access a module:
```py
import spam
spam.grok("hello")

from spam import grok
grok("hello")
```

For any function, it would record its definition environment, for which its module can be checked via `{func}.__module__`.

### Execution
- When a module is imported, all of the statements in the module execute one after another until the end of the file is reached
- The contents of the module namespace are all of the <ins>global</ins> names that are still defined at the end of the execution process
- If there are scripting statements that carry out tasks in the global scope (printing, creating files, etc.), output should be seen when `import` runs
- `import` always execute the __entire__ file, which means importing like `from math import sin` wouldn't have any efficiency gain than `import math`

### Cache
Modules only get loaded once at each session. Check `sys.modules` to see what cache is behind the scenes.

Nothing happens if a change applied to the source file then `import` is repeated during a session.

Even force-reload is possible like below:
```py
from importlib import reload
reload({module})
```
, it's not suggested to do so since zombie modules could be spawned in the meantime. For example, the modules imported by the reloaded module are not reloaded.



## Package
Package is a directory that contains multiple related files.

There are three types of import when in a package:
- Implicit Relative Import: `import {mod}`
- Absolute Import: `from {pack} import {mod}`
- Explicit Relative Import: `from . import {mod}`

Comparing all types of import above, it's preferred to apply _Explicit Relative Import_ since it not only averts package naming conflicts, but also avoids the hassle of package renaming. Though PEP-8 suggests _Absolute Import_ due to it predated over _Explicit Relative Import_, _Explicit Relative Import_ are used in the standard library.

`__init__.py` is mainly used to stitch multiple source files into a "unified" top-levelimport when desired. Leaving `__init__.py` empty is considered normal and even good practice under some scenarios.

Each submodule should define `__all__` to control the behavior of exporting `from {mod} import *`. An easy combination for submodules can be done via `__all__ = ({mod_a}.__all__ + {mod_b}.__all__)`


## Reference
- Modules and Packages: Live and Let Die: https://www.dabeaz.com/modulepackage/index.html
