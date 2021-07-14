
- [Development](#development)
  - [Initialization](#initialization)
- [Installation](#installation)
  - [Distribution](#distribution)
  - [Local](#local)
  - [Remote](#remote)
    - [Upload](#upload)
    - [Download](#download)
- [Demo](#demo)
- [Reference](#reference)


## Development

### Initialization
To mark a directory as a package, `__init__.py` needs to be created. Any directory with an `__init__.py` file is considered a Python package. The folder structure may look like:
```
caller/
  __init__.py
  a.py
  b.py
  c.py
```

If we want modules inside "caller" to be callable, importing statement(s) is(are) needed. For instance:
```py
from . import a
from . import c
```
So that others can utilize "caller" like `caller.a.xxx()` or `caller.c.xxx()`.

Note that `caller.b.xxx()` won't work since submoudle b wasn't included in `__init__.py`. However, submodule b can still be accessed via `from caller import b` to make `b.main()` functioning.


## Installation

### Distribution

Run `python setup.py sdist` to generate the source distribution, where _egg_ and _dist_ directories would be created.

To create the wheel distribution, package "wheel" is necessary. Then run `python setup.py bdist_wheel` to generate
distribution files. Check _build_ to verify if all modules and files needed for the distribution are included.

Both distributions have _egg_ and _dist_ directory. Though files inside _egg_ are the same, distribution via `sdist` is
a tar file, while that via `bdist_wheel` is a wheel file. Moreover, the wheel one includes _build_ directory.

Note that previous generated distribution would exist, so manual removal may be needed.

### Local

To quickly test whether the configuration of "setup.py" is correct, simply run `pip install -e .` under this root
project directory.

To install extra needed packages specified, run `pip install ".[extra]"` (double quote is recommended in case some
other shells like zsh fail to recognize).

### Remote

#### Upload

Normally, file "$HOME/.pypirc" would be used to define the configuration. Below is the
usual format:

```
[distutils]
  index-servers =
    default-repo
    testing-repo

[default-repo]
  repository = https://upload.pypi.org/legacy/
  username = {username}
  password = {password}

[testing-repo]
  repository = https://test.pypi.org/legacy/
  username = {username}
  password = {password}
```

Be cautious that "[distutils]" is mandatory for uploading to repository.

Looks like the API token mechanism in both official "pypi" repo are not working as expected,
the password should use the actual password since API token doesn't work.


When the configuration is done, command `python setup.py bdist_wheel upload -r default-repo`
would build the distribution and upload to the specified repo directly.

However, it's recommended to apply `twine` to take of the uploading. After the distribution
is generated, run `python -m twine upload --repository {repo} dist/*` to upload. For this
way, the process of distribution generation and uploading are separate, which is more manageable.

#### Download

Similar to the uploading, file "$HOME/.pip/pip.conf" is the one for downloading configuration:

```
[global]
  index-url =
    https://pypi.org/simple/

[install]
  index-url = https://test.pypi.org/simple/
  extra-index-url =
    {repo_1}
    {repo_2}
```

When it comes to download a package from a repo, it's worth to mention that there is certain
config precedence (command line > environment variable > configuration in ""). In that
case, `pip install` would look for the configuration following the precedence to download and install
the package specified.

So be aware of there is no environment variables like `PIP_INDEX_URL` or `PIP_EXTRA_INDEX_URL` if you
want the configuration file to take effect.

As long as the package is uploaded and the downloading configuration is properly set, then simply run
`pip install "{package[extra]}"` would do the work. Otherwise, run `pip install --index-url {repo} {package}` to
ensure the repo is correct.

For information:
- there can only one index url
- extra index url can be multiple



## Demo

Run codes below for demo to see if the package is function:

```py
import caller as demo
from caller import Animal
from caller import Fruit

demo.entry.main()

animal = Animal()
animal.printing()

fruit = Fruit()
fruit.printing()
```


## Reference
- Packaging Python Projects: https://packaging.python.org/tutorials/packaging-projects/
- Including Data Files: https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html#including-data-files
- The .pypirc file: https://packaging.python.org/specifications/pypirc/
- PIP Config Precedence: https://pip.pypa.io/en/stable/user_guide/#config-precedence
- Keywords in setuptools: https://setuptools.readthedocs.io/en/latest/references/keywords.html
- Metadata for Python Software Packages: https://www.python.org/dev/peps/pep-0314
- Specifying package versions: https://pip.pypa.io/en/stable/user_guide/#understanding-your-error-message
- Modules and Packages: Live and Let Die: https://www.dabeaz.com/modulepackage/index.html
- Packaging a python library: https://blog.ionelmc.ro/2014/05/25/python-packaging/
- Package Initialization: https://realpython.com/python-modules-packages/#package-initialization
- Structuring Your Project: https://docs.python-guide.org/writing/structure/
