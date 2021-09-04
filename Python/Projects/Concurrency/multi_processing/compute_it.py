#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demonstrate intensive CPU computation."""
from datetime import datetime
import math


def do_math(start=0, num=10) -> None:
    """Do the math by calculate in power then square root.

    Args:
        start: start number
        num: iteration times
    """
    pos = start
    k_sq = 1_000 * 1_000

    while pos < num:
        pos += 1
        dist = math.sqrt((pos - k_sq) * (pos - k_sq))

    print(dist)
    return


def main() -> None:
    """Execute the main workflow."""
    do_math(start=1)

    t0 = datetime.now()

    number = 30_000_000
    do_math(num=number)

    dt = datetime.now() - t0
    print(f"Done in {dt.total_seconds():,.2f} seconds.")

    return


if __name__ == "__main__":
    main()
