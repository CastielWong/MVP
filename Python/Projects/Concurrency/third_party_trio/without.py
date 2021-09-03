#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple demo to process jobs synchronously."""
from datetime import datetime
import random
import time

import colorama


def generate_data(num: int, data: list) -> None:
    """Generate data at every [0.5, 1.5] seconds.

    Args:
        num: number of times to generate data
        data: list of data generated
    """
    for idx in range(1, num + 1):
        item = idx * idx
        curr_time = datetime.now()

        data.append((item, curr_time))

        print(
            (f"{colorama.Fore.YELLOW}" f"--- generated record ({idx:-3}, {curr_time})"),
            flush=True,
        )
        time.sleep(random.random() + 0.5)  # nosec

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

        dt = datetime.now() - moment

        print(
            (
                f"{colorama.Fore.CYAN}"
                f"+++ Processed record ({item:-3}, {moment}) "
                f"after {dt.total_seconds():,.2f} seconds."
            ),
            flush=True,
        )
        time.sleep(0.5)

    return


def main() -> None:
    """Execute the main workflow."""
    t0 = datetime.now()
    print(f"{colorama.Fore.WHITE}App started.", flush=True)

    data: list = []
    generate_data(20, data)
    process_data(20, data)

    dt = datetime.now() - t0
    print(
        (
            f"{colorama.Fore.WHITE}"
            f"App exiting, total time: {dt.total_seconds():,.2f} seconds."
        ),
        flush=True,
    )

    return


if __name__ == "__main__":
    main()
