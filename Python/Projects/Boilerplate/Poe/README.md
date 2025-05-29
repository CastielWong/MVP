

- [Tool](#tool)
  - [Ruff](#ruff)
  - [Poetry](#poetry)
- [Task Runner](#task-runner)
- [Development](#development)
  - [Setup](#setup)
  - [Usage](#usage)
- [Publish](#publish)
- [Reference](#reference)


This boilerplate utilize [Poetry](https://python-poetry.org/) with [Poe the Poet](https://github.com/nat-n/poethepoet) for:
- auto formatting
- auto linting
- virtual environment
- dependency management
- package publish
- task runner



## Tool
### Ruff
Ruff is an extremely fast Python Linter and code formatter.

```sh
# perform formatting
ruff format
# perform linting
ruff check
```

### Poetry
Poetry is used for dependency management and packaging within its virtual environment.

```sh
# create a new project 'demo-proj'
poetry new --name demo-proj tmp_demo; cd tmp_demo
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

Plugin:
```sh
poetry self show plugins
poetry self add '{plugin}'
poetry self remove '{plugin}'
```

Dependency:
```sh
poetry show --tree --only {env}
poetry add --group {env} {packageA} {packageB}
poetry remove --group {env} {packageA} {packageB}
```


## Task Runner
"Poe the Poet" is used as task runner for Poetry.

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

Code formatting, linting and analysis:
```sh
# set pre-commit up
poetry add pre-commit --dev
poetry run pre-commit install
poetry run pre-commit autoupdate

# set wily up
poetry add wily -dev
# config for code analysis
poetry run wily setup
poetry run wily report

poetry run pre-commit run --all-files
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
The configurations are stored in:
- for global: "~/.config/pypoetry/config.toml"
- for local: "poetry.toml" under the project file

The authentication can be found in "~/.config/pypoetry/auth.toml".

```sh
# build the package
poetry build --output dist

# config the destination
# DEFAULT_PYPI="default-repo"
# poetry config pypi-token.${DEFAULT_PYPI}$ ${PYPI_API_TOKEN}
# poetry config repositories.${DEFAULT_PYPI} "https://upload.pypi.org/legacy/"

TEST_PYPI="test-pypi"
poetry config http-basic.${TEST_PYPI} "${TEST_PYPI_USER}" "${TEST_PYPI_PASS}" --local
poetry config repositories.${TEST_PYPI} "https://test.pypi.org/simple/" --local


poetry publish --repository ${TEST_PYPI}$ --dry-run
```

## Reference
- Configuration for PoeThePoet: https://github.com/nat-n/poethepoet/blob/main/pyproject.toml
