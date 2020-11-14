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
    name="packagingxxx",  # it can be the same as the module
    version="0.0.1",
    author="Anonymous",
    description="It's a MVP of Python packaging",
    long_description_content_type="text/markdown",
    long_description=long_description,
    keywords="demo testing laboratory",
    url=None,
    install_requires=required_packages,
    extras_require={
        "format": "pre-commit==2.8.0",
        "develop": ["virtualenv>=20.1.0", "urllib3~=1.26.0"],
    },
    packages=setuptools.find_packages(),
    include_package_data=True,  # it's necessary for MANIFEST.in to take effect
    python_required=">=3.6",
)
