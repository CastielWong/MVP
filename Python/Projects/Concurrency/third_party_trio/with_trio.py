#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demo a program running with `trio`.

trio.Queue was removed in v0.11.0:
- Replacing the call to trio.Queue() by trio.open_memory_channel()
- Using a MemorySendChannel object in generate_data function
- Using a MemoryReceiveChannel object in process_data function
- Updating requirements.txt with trio v0.16.0 and trio_asyncio v0.11.0
"""
from datetime import datetime
import random

from colorama import Fore
from trio import MemorySendChannel, MemoryReceiveChannel
import trio


async def generate_data(num: int, data: MemorySendChannel) -> None:
    """Generate data at asynchronous [0.0, 1.0] seconds.

    Args:
        num: number of times to generate data
        data: trio's channel of data generated
    """
    for idx in range(1, num + 1):
        curr_time = datetime.now()

        await data.send((idx, curr_time))

        print(f"{Fore.YELLOW}" f"--- Generated record ({idx:-2}, {curr_time})")
        await trio.sleep(random.random())  # nosec

    return


async def process_data(num: int, data: MemoryReceiveChannel) -> None:
    """Process data at every 0.5 second.

    Args:
        num: number of times to process
        data: trio's channel of data have been generated
    """
    processed = 0

    while processed < num:
        record = await data.receive()

        processed += 1
        item, moment = record

        elapsed = datetime.now() - moment

        print(
            f"{Fore.CYAN}+++ Processed record ({item:-2}, {moment}) "
            f"after {elapsed.total_seconds():,.2f} seconds."
        )
        await trio.sleep(0.5)

    return


async def main() -> None:
    """Execute the main workflow."""
    t0 = datetime.now()
    print(f"{Fore.WHITE}App started.")

    send_channel, receive_channel = trio.open_memory_channel(max_buffer_size=10)

    with trio.move_on_after(25):  # specify the upper time
        async with trio.open_nursery() as nursery:
            nursery.start_soon(generate_data, 20, send_channel, name="Producer 1")
            nursery.start_soon(generate_data, 20, send_channel, name="Producer 2")
            nursery.start_soon(process_data, 40, receive_channel, name="Consumer")

    elapsed = datetime.now() - t0
    print(
        f"{Fore.WHITE}App exiting, total time: {elapsed.total_seconds():,.2f} seconds."
    )

    return


if __name__ == "__main__":
    trio.run(main)
