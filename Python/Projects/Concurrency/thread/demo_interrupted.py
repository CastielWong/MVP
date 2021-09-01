#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demo how interruption works with threading."""
from datetime import datetime
import random
import time
import threading

import colorama


def check_cancel() -> None:
    """Check if there is cancel."""
    print(colorama.Fore.RED + "Press enter to cancel...", flush=True)
    input()

    return


def generate_data(num: int, data: list) -> None:
    """Generate data at asynchronous [0.5, 1.5] seconds.

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

    threads = [
        threading.Thread(target=generate_data, args=(20, data), daemon=True),
        threading.Thread(target=generate_data, args=(20, data), daemon=True),
        threading.Thread(target=process_data, args=(40, data), daemon=True),
    ]
    abort_thread = threading.Thread(target=check_cancel, daemon=True)
    abort_thread.start()

    for job in threads:
        job.start()

    while any((job.is_alive() for job in threads)):
        for job in threads:
            job.join(0.001)

        if not abort_thread.is_alive():
            print("Cancelling on your request!", flush=True)
            break

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
