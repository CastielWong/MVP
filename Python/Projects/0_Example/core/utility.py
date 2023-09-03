# -*- coding: utf-8 -*-
"""Utility module."""
from string import Template
import hashlib
import os

import numpy as np


def substitute_env_variable(string: str) -> str:
    """Fill in environment variable with actual value.

    Args:
        string: plain string with/without environment variable(s),
            when no such variable, it would keep the same and nothing to change

    Returns:
        String value which has environment variable(s) substituted
    """
    template = Template(string)
    new_value = template.safe_substitute(os.environ)
    return new_value


def format_float_with_precision(real: float) -> str:
    """Convert float to string with precision.

    By default, the output of a real number would be truncated to 6 decimal places,
    as well as keeping".0" if it's supposed to be an integer, or appending
    trailing 0(s) if such float number has less than 6 decimal places.

    When the real number has more than 6 decimal places, it would be outputted in
    scientific notation instead.

    This function is to ensure scientific notation won't be applied and all digits
    will be parsed into and kept as string.

    Args:
        real: float number, either in or not in scientific notation

    Returns:
        Converted string with all digits kept, without decimal point nor trailing 0
    """
    return np.format_float_positional(real, trim="-")


def calc_file_sha256(file_path: str) -> str:
    """Calculate the SHA256 digest for all contents inside a file.

    Args:
        file_path: path to the file for such calculation

    Returns:
        The SHA256 digest value
    """
    with open(file_path, "r", encoding="utf-8") as f_r:
        contents = f_r.read()
        digest = hashlib.sha256(contents.encode("utf-8"))

    return digest.hexdigest()
