
- [Setup](#setup)
    - [Pre-commit](#pre-commit)

This repo is used for MVP (Minimum Viable Product), which works more like a cache to quickly set up projects.

To push this repo from local to Github:

```sh
git remote add origin https://github.com/CastielWong/MVP.git
git push -u origin master
```


## Setup

### Pre-commit

It's a good practice to have [pre-commit](https://pre-commit.com/) in git repository for the purpose of code linting and formatting. Use Python to install and manage `pre-commit`. Its corresponding configuration is set in ".pre-commit-config.yaml".

```sh
pip install pre-commit
# check all files with pre-commit
pre-commit run --all-files

# set up pre-commit so that it would be triggered automatically whenever make an commit
pre-commit install
```
