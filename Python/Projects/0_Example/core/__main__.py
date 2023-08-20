#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point of the project."""
from core import utility as util

# pylint: disable=C0103(invalid-name)
if __name__ == "__main__":
    digest = util.calc_file_sha256("README.md")
    print(f"SHA256 digest for README.md is: {digest}")
