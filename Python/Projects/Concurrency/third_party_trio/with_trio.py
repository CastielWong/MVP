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

from trio import MemorySendChannel, MemoryReceiveChannel
import colorama
import trio


async def generate_data(num: int, data: MemorySendChannel) -> None:
    """Generate data at every [0.5, 1.5] seconds.

    Args:
        num: number of times to generate data
        data: trio's channel of data generated
    """
    for idx in range(1, num + 1):
        item = idx * idx
        curr_time = datetime.now()

        await data.send((item, curr_time))

        print(
            (f"{colorama.Fore.YELLOW}" f"--- generated record ({idx:-3}, {curr_time})"),
            flush=True,
        )
        await trio.sleep(random.random() + 0.5)  # nosec

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

        dt = datetime.now() - moment

        print(
            (
                f"{colorama.Fore.CYAN}"
                f"+++ Processed record ({item:-3}, {moment}) "
                f"after {dt.total_seconds():,.2f} seconds."
            ),
            flush=True,
        )
        await trio.sleep(0.5)


async def main() -> None:
    """Execute the main workflow."""
    t0 = datetime.now()
    print(f"{colorama.Fore.WHITE}App started.", flush=True)

    send_channel, receive_channel = trio.open_memory_channel(max_buffer_size=10)

    with trio.move_on_after(25):  # specify the upper time
        async with trio.open_nursery() as nursery:
            nursery.start_soon(generate_data, 20, send_channel, name="Producer 1")
            nursery.start_soon(generate_data, 20, send_channel, name="Producer 2")
            nursery.start_soon(process_data, 40, receive_channel, name="Consumer")

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
    trio.run(main)
