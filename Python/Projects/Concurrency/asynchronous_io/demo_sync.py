#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple demo to process jobs synchronously."""
from datetime import datetime
import random
import time

from colorama import Fore


def generate_data(num: int, data: list) -> None:
    """Generate data at every [0.0, 1.0] seconds.

    Args:
        num: number of times to generate data
        data: list of data generated
    """
    for idx in range(1, num + 1):
        curr_time = datetime.now()
        data.append((idx, curr_time))

        print(
            f"{Fore.YELLOW}--- Generated record ({idx:-2}, {curr_time})",
            flush=True,
        )
        time.sleep(random.random())  # nosec

    return


def process_data(num: int, data: list) -> None:
    """Process data at every 0.5 second.

    Args:
        num: number of times to process
        data: list of data have been generated
    """
    processed = 0

    while processed < num:
        record = data.pop(0)

        processed += 1
        item, moment = record

        elapsed = datetime.now() - moment

        print(
            (
                f"{Fore.CYAN}+++ Processed record ({item:-2}, {moment}) "
                f"after {elapsed.total_seconds():,.2f} seconds."
            ),
            flush=True,
        )
        time.sleep(0.5)

    return


def main() -> None:
    """Execute the main workflow."""
    t0 = datetime.now()
    print(f"{Fore.WHITE}App started.", flush=True)

    data: list = []
    generate_data(20, data)
    process_data(20, data)

    elapsed = datetime.now() - t0
    print(
        f"{Fore.WHITE}Finished, total time: {elapsed.total_seconds():,.2f} seconds.",
        flush=True,
    )

    return


if __name__ == "__main__":
    main()
