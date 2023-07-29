#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A setuptools based setup module.

See:
- https://packaging.python.org/guides/distributing-packages-using-setuptools
- https://github.com/pypa/sampleproject
"""
from typing import List
import os
import pathlib

import setuptools

PACKAGE_NAME = os.getenv("PACKAGE_NAME", "example_pacakge")
VERSION = os.getenv("PACKAGE_VERSION", "0.0.0")

PACKAGE_MAPPING = {PACKAGE_NAME: "core"}

HERE = pathlib.Path(__file__).parent.resolve()


def get_required_packages(file_name: str) -> List[str]:
    """Read packages required from file."""
    required_packages = []
    with open(file_name, "r", encoding="utf-8") as f_r:
        for line in f_r.readlines():
            if line.startswith("#") or "--" in line:
                continue
            required_packages.append(line)
    return required_packages


def get_installed_packages() -> List[str]:
    """Read packages to install from core."""
    installed_packages = []
    # iterate all modules in the packages to install
    for pck, subdir in PACKAGE_MAPPING.items():
        # include current package if it's a module
        dir_package = os.path.join(HERE, subdir)
        if "__init__.py" in os.listdir(dir_package):
            installed_packages.append(pck)

        modules = setuptools.find_namespace_packages(subdir)
        for module in modules:
            installed_packages.append(f"{pck}.{module}")

    return installed_packages


setuptools.setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="Example package for demonstration and reference",
    long_description=(HERE / "README.md").read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    author="Castiel Huang",
    author_email="wangyuh.castiel@gmail.com",
    maintainer="Castiel Huang",
    maintainer_email="wangyuh.castiel@gmail.com",
    install_requires=get_required_packages("requirements.txt"),
    extras_require={},
    url="https://github.com/CastielWong/MVP",
    keywords="python, best practice",
    packages=get_installed_packages(),
    package_dir=PACKAGE_MAPPING,
    include_package_data=True,
    # specify it as a universal wheel
    options={"bdist_wheel": {"universal": True}},
    python_requires=">=3.8, <4",
    project_urls={
        "README": (
            "https://github.com/CastielWong/MVP/tree/main/Python/Projects/0_Example"
        ),
    },
)
