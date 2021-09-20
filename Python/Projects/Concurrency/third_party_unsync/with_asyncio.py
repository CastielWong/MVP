#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demo a program running with `asyncio`."""
from datetime import datetime
import asyncio
import math

from colorama import Fore
from colorama.ansi import AnsiFore
import aiohttp
import requests


async def compute_some() -> None:
    """Perform computing intensive operation."""
    print(f"{Fore.YELLOW}Computing...")

    for _ in range(1, 10_000_000):
        math.sqrt(25 ** 25 + 0.01)

    return


async def download_some(url: str, color: AnsiFore = Fore.BLUE) -> None:
    """Perform network intensive operation.

    Args:
        url: url to download
        color: color to print
    """
    print(f"{color}Downloading...")

    async with aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(ssl=False)
    ) as session:
        async with session.get(url) as resp:
            resp.raise_for_status()

            text = await resp.text()

    print(f"{color}Length of characters downloaded: {len(text):,}.")

    return


async def download_some_more(url: str, color: AnsiFore = Fore.LIGHTBLUE_EX) -> None:
    """Perform more network intensive operation.

    Args:
        url: url to download
        color: color to print
    """
    print(f"{color}Downloading more ...")

    resp = requests.get(url)
    resp.raise_for_status()

    text = resp.text

    print(f"{color}Length of characters downloaded: {len(text):,}.")

    return


async def wait_some() -> None:
    """Simulate IO intensive operation."""
    print(f"{Fore.GREEN}Waiting...")

    for _ in range(1, 1_000):
        await asyncio.sleep(0.001)

    return


def main() -> None:
    """Execute the main workflow."""
    t0 = datetime.now()

    loop = asyncio.get_event_loop()

    tasks = []

    for _ in range(3):
        tasks.append(loop.create_task(compute_some()))

    for _ in range(2):
        tasks.append(
            loop.create_task(
                download_some(url="https://talkpython.fm/episodes/show/102")
            )
        )

    for _ in range(2):
        tasks.append(
            loop.create_task(
                download_some_more(url="https://pythonbytes.fm/episodes/show/92")
            )
        )

    for _ in range(4):
        tasks.append(loop.create_task(wait_some()))

    loop.run_until_complete(asyncio.gather(*tasks))

    elapsed = datetime.now() - t0
    print(
        f"{Fore.RESET}`asyncio` version done in {elapsed.total_seconds():,.2f} seconds."
    )

    return


if __name__ == "__main__":
    main()
