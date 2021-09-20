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

from colorama import Fore
import uvloop

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


async def generate_data(num: int, data: Queue, name: str = "Producer") -> None:
    """Generate data consecutively.

    Args:
        num: number of times to generate data
        data: list of data generated
        name: name of this task
    """
    message = f"{Fore.YELLOW}Starting {name}..."
    print(message)

    for idx in range(1, num + 1):
        curr_time = datetime.now()

        await data.put((idx, curr_time))
        await asyncio.sleep(0)

    return


async def process_data(num: int, data: Queue, name: str = "Consumer"):
    """Process data consecutively.

    Args:
        num: number of times to process
        data: list of data have been generated
        name: name of this task
    """
    message = f"{Fore.CYAN}Starting {name}..."
    print(message)

    processed = 0

    while processed < num:
        await data.get()
        processed += 1
        await asyncio.sleep(0)

    return


def main() -> None:
    """Execute the main workflow."""
    iterations = 50_000
    num_of_producers = 2

    t0 = datetime.now()
    print(f"Running standard loop with {iterations * num_of_producers:,} actions.")

    loop = asyncio.get_event_loop()
    data: Queue = Queue()

    producers = []
    for i in range(num_of_producers):
        producer = loop.create_task(
            generate_data(num=iterations, data=data, name=f"Producer {i+1}")
        )
        producers.append(producer)

    consumer = loop.create_task(
        process_data(num=iterations * num_of_producers, data=data)
    )

    task = asyncio.gather(consumer, *producers)
    loop.run_until_complete(task)

    elapsed = datetime.now() - t0
    print(f"{Fore.WHITE}Finished, total time: {elapsed.total_seconds():,.2f} seconds.")

    return


if __name__ == "__main__":
    main()
