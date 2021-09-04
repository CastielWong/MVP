#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demonstrate intensive CPU computation in multi-processing."""
from datetime import datetime
import math
import multiprocessing


def do_math(start=0, num=10) -> float:
    """Do the math by calculate in power then square root.

    Args:
        start: start number
        num: iteration times

    Returns:
        Average number
    """
    pos = start
    k_sq = 1_000 * 1_000
    ave = 0

    while pos < num:
        pos += 1
        val = math.sqrt((pos - k_sq) * (pos - k_sq))
        ave += val / num

    print(ave)
    return ave


def main() -> None:
    """Execute the main workflow."""
    do_math(start=1)

    t0 = datetime.now()

    number = 30_000_000

    processor_count = multiprocessing.cpu_count()
    print(f"Doing math on {processor_count} processors.")

    pool = multiprocessing.Pool()  # pylint: disable=R1732 (consider-using-with)
    tasks = []
    for index in range(1, processor_count + 1):
        task = pool.apply_async(
            do_math,
            (
                number * (index - 1) / processor_count,
                number * index / processor_count,
            ),
        )
        tasks.append(task)

    pool.close()
    pool.join()

    dt = datetime.now() - t0
    print(f"Done in {dt.total_seconds():,.2f} seconds.")

    print("Our results: ")
    for task in tasks:
        print(task.get())


if __name__ == "__main__":
    main()
