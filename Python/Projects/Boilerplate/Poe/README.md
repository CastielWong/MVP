

- [Poetry](#poetry)
  - [Poe the Poet](#poe-the-poet)
- [Development](#development)
  - [Setup](#setup)
  - [Usage](#usage)
- [Publish](#publish)


This boilerplate utilize [Poetry](https://python-poetry.org/) with [Poe the Poet](https://github.com/nat-n/poethepoet) for:
- auto formatting
- auto linting
- virtual environment
- dependency management
- package publish
- task runner


## Poetry
Poetry is used for dependency management and packaging within its virtual environment.

```sh
# create a new project
poetry new --src --name demo_src tmp_demo; cd tmp_demo
# check the virtual environment
poetry env info --path
# check available poetry virtual environment
poetry env list

# create a new virtual environment dedicated for the project
poetry env use python3

# add package needed, pyproject.toml would be updated automatically
poetry add "{package}>=x.x.x"


# set up environment from scratch
rm poetry.lock
poetry env remove --all
poetry install

# run the entrypoint
poetry run demoing

# run code in poetry environment
poetry run python -q
poetry run python -m pip list
```

### Poe the Poet
"Poe the Poet" is used as task runner in Poetry.

Configure tasks via YAML in "pyproject.toml":
```toml
[tool.poe.tasks]
test = "pytest"
auto-format = "ruff format ./ --config dev/ruff.toml"
auto-lint = "ruff check ./ --config dev/ruff.toml"

[tool.poe.tasks.check]
sequence = ["auto-format", "auto-lint"]
```

Run the task via
```sh
poetry poe check
```


## Development

### Setup
It's highly recommended to use `pipx` for `poetry` installation:
```sh
pip install --upgrade pip

pip install pipx

# clean up legacy poetry related stuff if any
rm poetry.lock
pipx uninstall poetry

# poetry can be found in `pipx list`
pipx install poetry
```

### Usage
Utilize "pip-tools" to manage package dependencies:
```sh
pip install pip-tools
pip-compile pyproject.toml --dry-run
```

Run commands below to kick off development:
```sh
rm poetry.lock
poetry env remove --all

# create a new virtual environment dedicated for the project
poetry env use python3

# install packages needed only (without packaging)
poetry install --no-root
```


## Publish
```sh
# build the package
poetry build --output dist

# config the destination
poetry config repositories.test_pypi 'https://test.pypi.org/simple' --local
poetry config http-basic.test_pypi '${TEST_PYPI_USER}' '${TEST_PYPI_PASS}' --local

poetry publish --repository test_pypi --dry-run
```
