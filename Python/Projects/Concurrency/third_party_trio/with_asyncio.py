#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demo a program running with `asyncio`."""
from asyncio import Queue
from datetime import datetime
import random
import asyncio

from colorama import Fore


async def generate_data(num: int, data: Queue) -> None:
    """Generate data at every [0.0, 1.0] seconds.

    Args:
        num: number of times to generate data
        data: asyncio's queue of data generated
    """
    for idx in range(1, num + 1):
        curr_time = datetime.now()

        await data.put((idx, curr_time))

        print(f"{Fore.YELLOW}" f"--- Generated record ({idx:-2}, {curr_time})")
        await asyncio.sleep(random.random())  # nosec

    return


async def process_data(num: int, data: Queue) -> None:
    """Process data at every 0.5 second.

    Args:
        num: number of times to process
        data: asyncio's queue of data have been generated
    """
    processed = 0

    while processed < num:
        record = await data.get()

        processed += 1
        item, moment = record

        elapsed = datetime.now() - moment

        print(
            f"{Fore.CYAN}+++ Processed record ({item:-2}, {moment}) "
            f"after {elapsed.total_seconds():,.2f} seconds."
        )
        await asyncio.sleep(0.5)

    return


def main() -> None:
    """Execute the main workflow."""
    t0 = datetime.now()
    print(f"{Fore.WHITE}App started.")

    loop = asyncio.get_event_loop()
    data = Queue()

    producer = loop.create_task(generate_data(20, data))
    consumer = loop.create_task(process_data(20, data))

    tasks = asyncio.gather(producer, consumer)
    loop.run_until_complete(tasks)

    elapsed = datetime.now() - t0
    print(
        f"{Fore.WHITE}App exiting, total time: {elapsed.total_seconds():,.2f} seconds."
    )

    return


if __name__ == "__main__":
    main()
