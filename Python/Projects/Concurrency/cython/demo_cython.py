#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demonstrate intensive CPU computation via Cython."""
from datetime import datetime
from threading import Thread
import multiprocessing

import math_core

TIME_SPENT_BASIC = 0.74


def main() -> None:
    """Execute the main workflow."""
    math_core.do_math(1)  # pylint: disable=I1101 (c-extension-no-member)

    t0 = datetime.now()

    # it's possible Cython would be overflowing when the number is too large
    number = 3_000_000

    processor_count = multiprocessing.cpu_count()
    print(f"Doing math on {processor_count} processors.")

    threads = []
    for index in range(1, processor_count + 1):
        threads.append(
            Thread(
                target=math_core.do_math,  # pylint: disable=I1101
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
    print(
        (
            f"Done in {dt.total_seconds():,.2f} seconds. "
            f"(factor: {TIME_SPENT_BASIC/dt.total_seconds():,.2f}x)"
        )
    )

    return


if __name__ == "__main__":
    main()
