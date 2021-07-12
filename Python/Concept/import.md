
- [Module](#module)
  - [Definition](#definition)
  - [Execution](#execution)
  - [Cache](#cache)
  - [Anatomy](#anatomy)
  - [Lazy Assembly](#lazy-assembly)
- [Import](#import)
  - [Type](#type)
  - [Execution Order](#execution-order)
  - [Implementation](#implementation)
  - [Tracking](#tracking)
- [Package](#package)
  - [Initialization](#initialization)
    - [Export Decorator](#export-decorator)
  - [Main](#main)
  - [Namespace Package](#namespace-package)
- [Path](#path)
  - [Deconstruction](#deconstruction)
  - [Customization](#customization)
  - [Script Directory](#script-directory)
- [Hacking](#hacking)
  - [Package Upgrade](#package-upgrade)
  - [Path Extend](#path-extend)
  - [User-Customized Plugin Directory](#user-customized-plugin-directory)
- [Reference](#reference)


For Python's interactive kernel, run `python -vv` to see verbose output, which contains information about initial importing.


## Module
Any python source file is considered as a __module__. A module is:
- A file of source code
- A namespace
- Container of global variables
- Execution environment for statements

What happens insidea mudule, stays in a module. If a file isn't on the `sys.path`, it won't be able to import.

Modules are fundamentally simple:
- modules are objects
- basically just a dictionary (globals)
- importing is juest `exec()` in disguise
- variations on import play with names
- tricky corner cases (threads, cycles, etc.)


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

```py
from importlib import reload
reload({module})
```
Even force-reload is possible like above, it's not suggested to do so since zombie modules could be spawned in the meantime. For example, the modules imported by the reloaded module are not reloaded.

The cache is a critical component of import. Advanced import-related code might have to interact with it directly.


### Anatomy
A module is an object, it can be created via:
```py
from types import ModuleType

mod = ModuleType("demo")
```
Check `mod.__dict__` to see what it contains. For an empty module, it would normally has attributes:
- `__name__`: module name
- `__doc__`: docstring
- `__spec__`: module spec
- `__loader__`: module loader
- `__package__`: package name

Other common attributes of a module object when imported:
- `__path__`: package path
- `__file__`: associated source file (if any)

A package is just a module with two defined (non-None) attributes:
- `__package__`: package name
- `__path__`: search path for subcomponents


### Lazy Assembly
To achieve Lazy Assembly, codes like below would be needed to placed in `__init__.py`:
```py
# list the exported symbols by module
_submodule_exports = {
  ".foo": ["Foo"],
  ".bar": ["Bar"]
}

# construct a {name: mod_name} mapping
# the example mapping is:
# {
#   "Foo": ".foo",
#   "Bar": ".bar"
# }
_submodule_by_name = {}
for module_name in _submodule_exports:
  for name in _submodule_exports[module_name]:
    _submodule_by_name[name] = module_name


from types import ModuleType
import importlib
import sys

class OnDemandModule(ModuleType):
  def __getattr__(self, name):
    module_name = _submodule_by_name.get(name)
    if module_name is None:
      raise AttributeError(f"No such '{name}' attribute")

    module = importlib.import_module(module_name, __package__)
    print(f"Loaded {name}")
    value = getattr(module, name)
    setattr(self, name, value)

    return value

# create a replacement module and have it inserted into `sys.modules`
new_module = OnDemandModule(__name__)
new_module.__dict__.update(globals())
new_module.__all__ = list(_submodule_by_name)
sys.modules[__name__] = new_module
```



## Import

### Type
There are three types of import when in a package:
- Implicit Relative Import: `import {mod}`
- Absolute Import: `from {pack} import {mod}`
- Explicit Relative Import: `from . import {mod}`

Comparing all types of import above, it's preferred to apply _Explicit Relative Import_ since it not only averts package naming conflicts, but also avoids the hassle of package renaming. Though PEP-8 suggests _Absolute Import_ due to it predated over _Explicit Relative Import_, _Explicit Relative Import_ are used in the standard library.


### Execution Order
The execution order of `import` is:
1. Create a module object
2. Execute source code inside the module
3. Assign the module object to a variable


### Implementation
Below is a minimal implementation of import:
```py
from types import ModuleType

def import_modules(mod_name):
  source_path = mod_name + ".py"
  with open(source_path, "r") as fr:
    source_code = fr.read()
  mod = ModuleType(mod_name)
  mod.__file__ = source_path
  code = compile(source_code,source_path, "exec")
  exec(code, mod.__dict__)

  return mod
```

Implementation of import which exerts cache:
```py
from types import ModuleType
import dis
import sys

def import_modules(mod_name):
  if mod_name in sys.modules:
    return sys.modules[mod_name]

  source_path = mod_name + ".py"
  with open(source_path, "r") as fr:
    source_code = fr.read()
  mod = ModuleType(mod_name)
  mod.__file__ = source_path

  sys.modules[mod_name] = mod

  code = compile(source_code, source_path, "exec")
  exec(code, mod.__dict__)

  # dis.dis(code) # if disasembling wanted

  return sys.modules[mod_name]
```

Since `import` can be used and buried inside functions, try to avoid such importing, which could cause concurrent imports when threading is involved.


### Tracking
`__import__()` is a built-in function, a module/package can be imported via `__import__("{mod}", globals, None, None, 0)` or `__import__("{mod}")` if such module is available under current working directory.

Another better alternative is to utilize `importlib.import_module()`, for example:
```py
# equivalent to `import demo`
demo = importlib.import_module("demo")

# equivalent to `from . import demo`
demo = importlib.import_module("demo", __package__)
```

Track how a new import imports other relative imports:
```py
def track_imports(mod_name, *args, imp=__import__):
  print(f"importing {mod_name}")
  return imp(mod_name, *args)
```

Then replace the built-in `__import__` with the new one, imports tracking should be enabled when new imports in:
```py
import builtins
builtins.__import__ = track_imports

import {mod}
```



## Package
Package is a directory that contains multiple related files.

### Initialization
`__init__.py` is the initialization file for each pacakge. It is mainly used to stitch multiple source files into a "unified" top-levelimport when desired. Leaving `__init__.py` empty is considered normal and even good practice under some scenarios.

Note that `__init__.py` connotes initialization, but not implementation. So it's bad practice to put everything inside `__init__.py`。

Each submodule should define `__all__` to control the behavior of exporting `from {mod} import *`. An easy combination for submodules can be done via `__all__ = ({mod_a}.__all__ + {mod_b}.__all__)`

#### Export Decorator
Depending on the requirements, it maybe easier to apply decorator to tag the exported definitions, for which the decorator can be created at `__init__.py`
```py
def export(defn):
  globals()[defn.__name__] = defn
  __all__.append(defn.__name__)
  return defn
```

With such decorator, it clearly marked in the source code which function is expected to be exported.

Some points to be considered when applying the export decorator:
- Whether it's expected or worth to have `from . import export` all over the project
- For large framework, cost on the performance can be expensive

### Main
Assuming the project structure is like below:
```
spam/
  __init__.py
  foo.py
```
And "foo.py" has relative import statements inside.

Note that `python -m spam.foo` would be working, but `python spam/foo.py` wouldn't, since the latter would throw `ImportError: attempted relative import with no known parent package`.

`__main__.py` is not only used to designate main for a package, but also makes a package directory executable. It marks the entry point for the package explicitly. With `__main__.py`, either `python -m {package}` or `python {package}` should be working. And it's also a useful organizational tool.

An interesting thing is that `__main__.py` works for a directory as well, which means Python can execute a raw directory if there is a file called `__main__.py`.


### Namespace Package
A directory without `__init__.py` is considered to be a Namespace Package.

Suppose there are two directories with the same name yet under different folders, for both contain the same top-level package name but different subparts:
```
spam_foo/
  spam/
    foo.py
spam_bar/
  spam/
    bar.py
```

Putting both directories in `sys.path` via `sys.path.extend(["spam_foo", "spam_bar])`, then code below would work:
```py
import spam.foo
import spam.bar
```
Which shows that two directories "become" one.

The reason is that package has a builtin variable called `__path__`, which is a list of directories searched for submodules. For a Namespace Package, all matching paths get collected. For the example above, the list of `spam__path__` is "_NamespaecPath(["spam_foo/spam", "spam_bar/spam"])".

Note that it only works if there is no `__init__.py` in top level.

Namespace packages might be useful for framework builders who want to maintain its own third-party plugin system, like User-Customized Plugin Directory.

Applying namespace packages is not considered to be a good practice.


## Path
Almost every tricky problem concerning modlues/packages is related to `sys.path`. As long as such module/package doesn't exist in `sys.path`, it wouldn't be able to be imported.

`sys.path` has following mechanism:
- It's a list of strings:
  - direcotry name
  - name of a .zip file, which work as if it's a normal directory
  - name of an .egg file, which is actually just a directory or .zip file with extra metadata
- It traverses start-to-end looking for imports
- The __first match__ get imported
- It's constructed from three parts:
  - `sys.prefix`
  - __PYTHONPATH__
  - "site.py"

The environment variable __PYTHONHOME__ overrides the path configuration in `sys`. ”Fatal Python error“ with the list of path configuration would be returned if __PYTHONHOME__ is invalid and `python` is run.

### Deconstruction
Run `python -S` to skip "site.py" initialization, which `sys.site` would show the location of standard library. Be aware of that `exit()` is a function came from module `_sitebuiltins`, which means `exit()` wouldn't work and "Ctrl + D" is needed to shut down the Python interpreter.

`sys.prefix` specifies base location of Python installation `sys.exec_prefix` is location of compiled binaries by C.

Python standard libraries usually located at:
- `sys.prefix` + "/lib/python3X.zip"
- `sys.prefix` + "/lib/python3.X"
- `sys.prefix` + "/lib/python3.X/plat-sysname"
- `sys.exec_prefix` + "/lib/python3.X/lib-dynload"

Certain library files must exist for Python's searches:
- python or python3: python executable
- os.py: landmark for `sys.prefix`
- lib-dynload/: landmark for `sys.exec_prefix`

Suppose Python is located at ”/Users/demo/software/bin/python3“, then:
- `sys.prefix` would search at (.pyc files included)
  - /Users/demo/software/lib/python3.x/os.py
  - /Users/demo/lib/python3.x/os.py
  - /Users/lib/python3.x/os.py
  - /lib/python3.x/os.py
- `sys.executable` would search at
  - /Users/demo/software/lib/python3.x/lib-dynload/
  - /Users/demo/lib/python3.x/lib-dynload/
  - /Users/lib/python3.x/lib-dynload/
  - /lib/python3.x/lib-dynload/


### Customization
Control of `sys.prefix` is a major part of tools that package Python in custom ways. `sys.prefix` would check in the following order:
- environment variable check
- "installation" landmarks
- virtual environments

Set environment variable __PYTHONPATH__ to add customized path to `sys.path`. Paths in __PYTHONPATH__ would go first in `sys.path` list.

Any third-party module directories, which should be "site-packages", would be added by "site.py".

"site-packages" directories would be existed at:
- "/usr/local/lib/python3.x/site-packages/" when run `pip install`
- "/User/demo/.local/lib/python3.x/site-packages/" when run `pip install --user`
- "/usr/local/lib/python3.x/dist-packages/" for some Linux distros


### Script Directory
The first path component in `sys.path` is the same directory as the running script, which gets added last.



## Hacking
When it comes to import, Python has quite "flexible" ways to work around.

Though hacking ways below are all possible and feasible, it's highly suggested to avoid them. As the Python expert David Beazley's adviced: "Stay away. Far away."


### Package Upgrade
A package can "upgrade" itself during import. For example, the `__init__.py` of "xml" package in Python 2.7:
```py
try:
  import _xmlplus
  import sys
  sys.modules[__name__] = _xmlplus
except ImportError:
  pass
```


### Path Extend
Creating .pth files can be used to extend `sys.path`. Moving .pth files to any "site-packages" direcotory, then all directories that exist would be added to `sys.path`. If such directory doesn't exist, it wouldn't be appended.

Mainly, .pth files used by package managers to install packages in addtional directories.

Note that any line starting with "import" in .pth file would be executed . Package managers and extensions can use it to perform automagic steps upon Python startup, which requires no patching of other files.


### User-Customized Plugin Directory
Assuming the file system layout is below:
```
demo/
  __init__.py
  fruit/
    apple.py
~/
  .demo/
    b/
      fruit/
        banana.py
    c/
      fruit/
        cherry.py
```

Namespace Package can be used to make it workable like the logical package below:
```
demo/
  __init__.py
  fruit/
    apply.py
    banana.py
    cherry.py
```

Inisde `demo/__init__.py`, create the namespace package subcomponent by merging a system install with user-plugins:
```py
...
__path__ = [
  "demo/fruit",
  "/User/demo/.demo/b/fruit",
  "/User/demo/.demo/c/fruit"
]
```

The actual hacking implementation is:
```py
import os

user_plugins = os.path.expanduser("~/.demo")
if os.path.exists(user_plugins):
  plugins = os.listdir(user_plugins)
  for plugin in plugins:
    __path__.append(os.path.join(user_plugins, plugin))
```



## Reference
- Modules and Packages: Live and Let Die: https://www.dabeaz.com/modulepackage/index.html
