# -*- coding: utf-8 -*-
"""The core module to perform the math operation in Cython."""
from libc.math cimport sqrt

from colorama import Fore
from colorama.ansi import AnsiFore
import cython


def do_math(start: cython.int = 0, stop: cython.int = 10, color: AnsiFore = Fore.RESET) -> cython.float:
    """Do the math by calculate in power then square root.

    Args:
        start: start number
        stop: number until stop
        color: printing color

    Returns:
        Average over the calculated difference
    """
    summation = 0.0

    position: cython.int = start
    k_sq: cython.float = 1000 * 1000

    print(f"{color}This thread is taking care of range: [{start:,}, {stop:,})")

    with nogil:
        while position < stop:
            position += 1
            diff = sqrt((position - k_sq) * (position - k_sq))

            summation += diff

        average = summation / (stop - start)
    print(f"{color}Result when position {position:>10,} is reached: {average:>15,.3f}")

    return
