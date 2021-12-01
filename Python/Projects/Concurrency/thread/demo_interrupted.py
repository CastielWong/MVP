#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demo how interruption works with threading."""
from datetime import datetime
import random
import time
import threading

from colorama import Fore


def check_cancel() -> None:
    """Check if there is cancel."""
    print(Fore.RED + "Press enter to cancel...")
    # monitor and capture input
    # so that it would return when enter is pressed
    input()

    return


def generate_data(num: int, data: list) -> None:
    """Generate data at asynchronous [0.0, 1.0] seconds.

    Args:
        num: number of times to generate data
        data: list of data generated
    """
    for idx in range(1, num + 1):
        curr_time = datetime.now()

        data.append((idx, curr_time))

        print(f"{Fore.YELLOW}--- Generated record ({idx:-3}, {curr_time})")
        time.sleep(random.random())  # nosec

    return


def process_data(num: int, data: list) -> None:
    """Process data when there is.

    Args:
        num: number of times to process
        data: list of data have been generated
    """
    processed = 0

    while processed < num:
        record = None

        if data:
            record = data.pop(0)

        if not record:
            time.sleep(0.01)
            continue

        processed += 1
        item, moment = record

        elapsed = datetime.now() - moment

        print(
            f"{Fore.CYAN}+++ Processed record ({item:-3}, {moment}) "
            f"after {elapsed.total_seconds():,.2f} seconds."
        )
        time.sleep(0.5)

    return


def main() -> None:
    """Execute the main workflow."""
    t0 = datetime.now()
    print(f"{Fore.WHITE}App started.")

    data: list = []

    jobs = [
        threading.Thread(target=generate_data, args=(20, data), daemon=True),
        threading.Thread(target=process_data, args=(20, data), daemon=True),
    ]

    abort_thread = threading.Thread(target=check_cancel, daemon=True)
    abort_thread.start()

    for thread in jobs:
        thread.start()
        thread.join(0.001)

    while any(thread.is_alive() for thread in jobs):
        if abort_thread.is_alive():
            continue

        # stop when the abort thread is triggered
        print("Cancelling on your request!")
        break

    elapsed = datetime.now() - t0
    print(
        f"{Fore.WHITE}App exiting, total time: {elapsed.total_seconds():,.2f} seconds."
    )

    return


if __name__ == "__main__":
    main()
