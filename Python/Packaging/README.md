
- [Installation](#installation)
    - [Distribution](#distribution)
    - [Local](#local)
    - [Remote](#remote)
        - [Upload](#upload)
        - [Download](#download)
- [Demo](#demo)
- [Reference](#reference)

## Installation

### Distribution

Run `python setup.py sdist` to generate the source distribution, where _egg_ and _dist_ directories would be created.

To create the wheel distribution, package "wheel" is necessary. Then run `python setup.py bdist_wheel` to generate
distribution files. Check _build_ to verify if all modules and files needed for the distribution are included.

Both distributions have _egg_ and _dist_ directory. Though files inside _egg_ are the same, distribution via `sdist` is
a tar file, while that via `bdist_wheel` is a wheel file. Moreover, the wheel one includes _build_ directory.

Note that previous generated distribution would exist, so manual removal may be needed.

### Local

To quickly test whether the configuration of "setup.py" is correct, simply run `pip install .` under this root
project directory.

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
`pip install {package}` would do the work. Otherwise, run `pip install --index-url {repo} {package}` to
ensure the repo is correct.


## Demo

Run codes below for demo to see if the package is function:

```py
import caller as demo
from caller import Fruit

demo.entry.main()

fruit = Fruit()
fruit.printing()
```


## Reference

- Packaging Python Projects: https://packaging.python.org/tutorials/packaging-projects/
- Including Data Files: https://setuptools.readthedocs.io/en/latest/userguide/quickstart.html#including-data-files
- The .pypirc file: https://packaging.python.org/specifications/pypirc/
- PIP Config Precedence: https://pip.pypa.io/en/stable/user_guide/#config-precedence
