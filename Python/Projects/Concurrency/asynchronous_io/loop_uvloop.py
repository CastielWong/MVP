#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demo the efficiency of uvloop.

uvloop is a fast, drop-in replacement of the built-in asyncio event loop.
uvloop and asyncio, combined with the power of async/await, makes it easier than ever
to write high-performance networking code in Python.
"""
from asyncio import Queue
from datetime import datetime
import asyncio

import colorama
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def generate_data(num: int, data: Queue) -> None:
    """Generate data consecutively.

    Args:
        num: number of times to generate data
        data: list of data generated
    """
    for idx in range(1, num + 1):
        item = idx * idx
        curr_time = datetime.now()

        await data.put((item, curr_time))
        await asyncio.sleep(0)

    return


async def process_data(num: int, data: asyncio.Queue):
    """Process data consecutively.

    Args:
        num: number of times to process
        data: list of data have been generated
    """
    processed = 0

    while processed < num:
        await data.get()
        processed += 1
        await asyncio.sleep(0)

    return


def main() -> None:
    """Execute the main workflow."""
    lim = 150_000

    t0 = datetime.now()
    print(f"Running standard loop with {lim * 2:,} actions.")

    loop = asyncio.get_event_loop()
    data = Queue()

    task1 = loop.create_task(generate_data(lim, data))
    task3 = loop.create_task(generate_data(lim, data))
    task2 = loop.create_task(process_data(2 * lim, data))

    final_task = asyncio.gather(task1, task2, task3)
    loop.run_until_complete(final_task)

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
