#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fr:
    long_description = fr.read()

required_packages = []
with open("requirements.txt", "r") as fr:
    for line in fr.read().splitlines():
        # skip any comment/command line
        if line.startswith("#") or "--" in line:
            continue

        required_packages.append(line)

setuptools.setup(
    name="packaging-xxx",  # it can be the same as the module
    version="0.0.1",
    author="Anonymous",
    description="It's a MVP of Python packaging",
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_required=required_packages,
    extra_requirement={"develop": "virtualenv", "format": ["pre-commit"]},
    url=None,
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_required=">=3.6",
)
