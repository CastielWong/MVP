

- [Development](#development)
- [Installation](#installation)
- [Importing](#importing)
  - [CWD](#cwd)
- [Reference](#reference)

This section is to save all MVPs and cached knowledge related to Python.

## Development
Run `source init.sh` to initialize environment for development.


## Installation
Install Python in Linux is a bit trivial, commands below should be more than enough to install Python successfully.

```sh
yum install gcc openssl-devel bzip2-devel libffi-devel -y

wget https://www.python.org/ftp/python/3.x.x/Python-3.x.x.tgz
tar -xzf Python-3.x.x.tgz

./configure --enable-optimizations
make altinstall
```

## Importing
In Python, importing modules or packages can be genuinely annoying if not planned well.

The general order for Python to seach for modules and packages to import:
1. built-in modules from Python Standard Library, such as `os`, `sys`, `math`
2. modules or packages in a directory specified by `sys.path`:
   - in interactive python shell, `sys.path[0]` is the empty string `''`, which asks Python to search in current working directory (the one when `python` is run)
   - run in python script like `python {script}.py`, `sys.path[0]` should be the path/directory of "{script}.py"
3. modules or packages in a directory specified by the environment variable `PYTHONPATH`

Note that "current working directory" for `sys.path` is the directory where the current python script is run.

### CWD
__CWD__(Current Working Directory) can be ambiguous, at least it can refer to three different location:
- A: directory that current shell is on
- B: directory that contains the script run
- C: directory that contains the root script which calls the script to run

Assuming the project structure is as below:
```
proj/
    pack_a/
        subpack_1/
            innermost.py
        inner.py
    outer.py
```
"inner.py" imports "innermost.py", and "innermost.py" will print `sys.path` whenever it run or is imported.

Running `python pack_a/inner.py`, then the __CWD__ can be referred to:
- A: "proj/"
- B: "proj/pack_a/subpack_1/"
- C: "proj/pack_a/"

`sys.path[0]` should be the option C, which is "proj/pack_a/" in this case.



## Reference
- How to Install Python 3: https://www.liquidweb.com/kb/how-to-install-python-3-on-centos-7/
- The Definitive Guide to Python import Statements: https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
