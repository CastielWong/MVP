
- [Installation](#installation)
    - [Local](#local)
- [Reference](#reference)

## Installation

### Local

To quickly test whether the configuration of "setup.py" is correct, simply run `pip install .` under this root
project directory.

Run codes below to invoke the module function:
```py
from caller import entry

entry.main()
entry.load_data()
```

Run `python setup.py sdist` to generate the source distribution, where _egg_ and _dist_ directories would be created.

To create the wheel distribution, package "wheel" is necessary. Then run `python setup.py bdist_wheel` to generate
distribution files. Check _build_ to verify if all modules and files needed for the distribution are included.

Both distributions have _egg_ and _dist_ directory. Though files inside _egg_ are the same, distribution via `sdist` is
a tar file, while that via `bdist_wheel` is a wheel file. Moreover, the wheel one includes _build_ directory.


## Reference

- Packaging Python Projects: https://packaging.python.org/tutorials/packaging-projects/
- Including Data Files: https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html#including-data-files
