# -*- coding: utf-8 -*-
"""The core module to perform the math operation in Cython."""
from libc.math cimport sqrt

import cython


def do_math(start: cython.float = 0, num: cython.float = 10) -> None:
    """Do the math by calculate in power then square root.

    Args:
        start: start number
        num: iteration times
    """
    pos: cython.float = start
    k_sq: cython.float = 1000 * 1000

    with nogil:
        while pos < num:
            pos += 1
            sqrt((pos - k_sq) * (pos - k_sq))

    return
