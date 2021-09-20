#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demonstrate intensive CPU computation via Cython."""
from datetime import datetime
from threading import Thread
import multiprocessing

from colorama import Fore
import math_core

TIME_SPENT_BASIC = 0.74

# note that it's possible Cython would be overflowing when the number is too large
NUMBER = 3_000_000


def main() -> None:
    """Execute the main workflow."""
    t0 = datetime.now()

    color_mapping = {
        0: Fore.YELLOW,
        1: Fore.CYAN,
        2: Fore.GREEN,
        3: Fore.MAGENTA,
    }

    processor_count = multiprocessing.cpu_count()
    print(f"Doing math on {processor_count} processors.")

    processor_count = min(processor_count, 4)
    print(f"Doing math on {processor_count} processors.")

    tasks = []
    for index in range(processor_count):
        task = Thread(
            target=math_core.do_math,  # pylint: disable=I1101
            args=(
                int(NUMBER * index / processor_count),
                int(NUMBER * (index + 1) / processor_count),
                color_mapping[index],
            ),
            daemon=True,
        )
        tasks.append(task)

    for thread in tasks:
        thread.start()

    for thread in tasks:
        thread.join()

    elapsed = datetime.now() - t0
    print(f"{Fore.RESET}Done in {elapsed.total_seconds():,.2f} seconds. ")
    print(f"(factor: {TIME_SPENT_BASIC / elapsed.total_seconds():,.2f}x)")

    return


if __name__ == "__main__":
    main()
