#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""A simple demo to asyncio."""
from asyncio import Queue
from datetime import datetime
import asyncio
import random

import colorama


async def generate_data(num: int, data: Queue) -> None:
    """Generate data at asynchronous [0.5, 1.5] seconds.

    Args:
        num: number of times to generate data
        data: list of data generated
    """
    for idx in range(1, num + 1):
        item = idx * idx
        curr_time = datetime.now()

        await data.put((item, curr_time))

        print(
            (f"{colorama.Fore.YELLOW}" f"--- generated record ({idx:-3}, {curr_time})"),
            flush=True,
        )
        await asyncio.sleep(random.random() + 0.5)  # nosec

    return


async def process_data(num: int, data: Queue):
    """Process data at asynchronous 0.5 second.

    Args:
        num: number of times to process
        data: list of data have been generated
    """
    processed = 0

    while processed < num:
        record = await data.get()

        processed += 1
        item, moment = record

        dt = datetime.now() - moment

        print(
            (
                f"{colorama.Fore.CYAN}"
                f"+++ Processed record ({item:-3}, {moment}) "
                f"after {dt.total_seconds():,.2f}s."
            ),
            flush=True,
        )
        await asyncio.sleep(0.5)

    return


def main() -> None:
    """Execute the main workflow."""
    loop = asyncio.get_event_loop()

    t0 = datetime.now()
    print(f"{colorama.Fore.WHITE}App started.", flush=True)

    data: Queue = Queue()

    task1 = loop.create_task(generate_data(20, data))
    task2 = loop.create_task(generate_data(20, data))
    task3 = loop.create_task(process_data(40, data))

    final_task = asyncio.gather(task1, task2, task3)
    loop.run_until_complete(final_task)

    dt = datetime.now() - t0
    print(
        f"{colorama.Fore.WHITE}"
        f"App exiting, total time: {dt.total_seconds():,.2f} sec.",
        flush=True,
    )


if __name__ == "__main__":
    main()
