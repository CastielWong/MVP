#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demonstrate intensive CPU computation."""
from datetime import datetime
import math

from colorama import Fore
from colorama.ansi import AnsiFore

NUMBER = 3_000_000


def do_math(start: int = 0, stop: int = 10, color: AnsiFore = Fore.RESET) -> float:
    """Overload CPU computation by calculating number in power then square root.

    Args:
        start: start number
        stop: number until stop
        color: printing color

    Returns:
        Average over the calculated difference
    """
    summation = 0.0

    position = start
    # set a fair number to increase computation consumption
    k_sq = 1_000 * 1_000

    print(f"{color}This thread is taking care of range: [{start:,}, {stop:,})")

    while position < stop:
        if position % 2_000_000 == 0:
            print(f"{color}Computing reaches to position {position:>15,}...")

        position += 1
        diff = math.sqrt((position - k_sq) * (position - k_sq))

        summation += diff

    average = summation / (stop - start)
    print(
        f"{Fore.RESET}"
        f"Result when position {position:>10,} is reached: {average:>15,.3f}"
    )

    return average


def main() -> None:
    """Execute the main workflow."""
    t0 = datetime.now()

    do_math(stop=NUMBER, color=Fore.YELLOW)

    elapsed = datetime.now() - t0
    print(f"Done in {elapsed.total_seconds():,.2f} seconds.")

    return


if __name__ == "__main__":
    main()
