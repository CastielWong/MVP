#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demonstrate intensive CPU computation in multi-threading."""
from datetime import datetime
from threading import Thread
import math
import multiprocessing


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

    processor_count = multiprocessing.cpu_count()
    print(f"Doing math on {processor_count} processors.")

    threads = []
    for index in range(1, processor_count + 1):
        threads.append(
            Thread(
                target=do_math,
                args=(
                    number * (index - 1) / processor_count,
                    number * index / processor_count,
                ),
                daemon=True,
            )
        )

    for job in threads:
        job.start()

    for job in threads:
        job.join()

    dt = datetime.now() - t0
    print(f"Done in {dt.total_seconds():,.2f} seconds.")

    return


if __name__ == "__main__":
    main()
