#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sample configuration file."""
# pylint: skip-file
import os
import sys

# ensure this configuration is available in python path
# note this "conf.py" will be placed under root directory
sys.path.insert(0, os.path.abspath("contents"))

project = "Demo Siting"
copyright = "2022, Castiel"
author = "Castiel"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
html_static_path = ["_static"]
templates_path = ["_templates"]

myst_enable_extensions = [
    "colon_fence",
]
