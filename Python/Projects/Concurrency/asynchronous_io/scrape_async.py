#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demo to process web scrping asynchronously."""
from datetime import datetime
import asyncio

from colorama import Fore
import aiohttp
import bs4

# Older versions of python require calling LOOP.create_task() rather than
# on asyncio.Make this available more easily.
LOOP = asyncio.get_event_loop()


async def get_html(episode_number: int) -> str:
    """Get html of the corresponding episode number.

    Args:
        episode_number: the episode number

    Returns:
        Text in HTML
    """
    print(f"{Fore.YELLOW }Getting HTML for episode {episode_number}", flush=True)

    url = f"https://talkpython.fm/{episode_number}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()

            return await resp.text()


def get_title(html: str, episode_number: int) -> str:
    """Get title of the corresponding episode number.

    Args:
        html: content of html page
        episode_number: the episode number

    Returns:
        Title of the episode
    """
    print(f"{Fore.CYAN}Getting TITLE for episode {episode_number}", flush=True)

    soup = bs4.BeautifulSoup(html, "html.parser")
    header = soup.select_one("h1")

    if not header:
        return "MISSING"

    return header.text.strip()


async def get_title_range_no_loop():
    """Get titles of the specified range."""
    for e_n in range(150, 160):
        html = await get_html(e_n)
        title = get_title(html, e_n)

        print(f"{Fore.WHITE}Title found: {title}", flush=True)

    return


async def get_title_range_with_loop():
    """Get titles of the specified range with loop involved."""
    tasks = []
    for e_n in range(150, 160):
        tasks.append((e_n, LOOP.create_task(get_html(e_n))))

    for e_n, task in tasks:
        html = await task
        title = get_title(html, e_n)
        print(f"{Fore.WHITE}Title found: {title}", flush=True)


def main() -> None:
    """Execute the main workflow."""
    t0 = datetime.now()

    # loop.run_until_complete(get_title_range_no_loop())
    LOOP.run_until_complete(get_title_range_with_loop())

    dt = datetime.now() - t0
    print(f"Done in {dt.total_seconds():.2f} sec.")

    return


if __name__ == "__main__":
    main()
