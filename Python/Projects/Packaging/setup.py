#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import setuptools

DIR_ROOT = os.path.dirname(__file__)

PACKAGE_MAPPING = {"package_name": "caller"}

with open("README.md", "r") as fr:
    long_description = fr.read()

required_packages = []
with open("requirements.txt", "r") as fr:
    for line in fr.read().splitlines():
        # skip any comment/command line
        if line.startswith("#") or "--" in line:
            continue

        required_packages.append(line)

installed_packages = []
# iterate all modules in the packages to collect
# those needed to install
for pck, subdir in PACKAGE_MAPPING.items():
    # include current package if it's a module
    dir_package = os.path.join(DIR_ROOT, subdir)
    if "__init__.py" in os.listdir(dir_package):
        installed_packages.append(pck)

    modules = setuptools.find_namespace_packages(subdir)
    for mod in modules:
        installed_packages.append(f"{pck}.{mod}")

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
    packages=installed_packages,
    package_dir=PACKAGE_MAPPING,
    include_package_data=True,  # it's necessary for MANIFEST.in to take effect
    options={"bdist_wheel": {"universal": True}},
    python_required=">=3.6",
)
