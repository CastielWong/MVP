#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demonstrate how to easily swop between multithreading and multiprocessing."""
from concurrent.futures import Future
from concurrent.futures.process import ProcessPoolExecutor
from concurrent.futures.thread import ThreadPoolExecutor
import multiprocessing

from colorama import Fore
import requests
import bs4


def get_title(url: str) -> str:
    """Get html of the corresponding episode number.

    Args:
        episode_number: the episode number

    Returns:
        Text in HTML
    """
    process = multiprocessing.current_process()
    print(
        f"{Fore.YELLOW}Getting title from {url:<30} | "
        f"PID: {process.pid:>8} | ProcName: {process.name}"
    )

    resp = requests.get(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:61.0) "
                "Gecko/20100101 Firefox/61.0"
            )
        },
    )
    resp.raise_for_status()

    html = resp.text

    soup = bs4.BeautifulSoup(html, features="html.parser")
    tag: bs4.Tag = soup.select_one("h1")

    prefix = f"From {url:<30}:"
    if not tag:
        return f"{prefix} NONE"

    if not tag.text:
        anchor = tag.select_one("a")
        if anchor and anchor.text:
            return f"{prefix} {anchor.text}"

        if anchor and "title" in anchor.attrs:
            return f"{prefix} {anchor.attrs['title']}"

        return f"{prefix} NONE"

    return f"{prefix} {tag.get_text(strip=True)}"


def main(mode: str) -> None:
    """Execute the main workflow.

    Args:
        mode: either "process" or "thread"
    """
    pool_executor = {
        "process": ProcessPoolExecutor(),
        "thread": ThreadPoolExecutor(),
    }
    print(f"Running in mode: {Fore.GREEN}{mode}")

    urls = [
        "https://talkpython.fm",
        "https://pythonbytes.fm",
        "https://google.com",
        "https://realpython.com",
        "https://training.talkpython.fm",
    ]

    work = []

    with pool_executor[mode] as executor:
        for url in urls:
            future: Future = executor.submit(get_title, url)
            work.append(future)

        print(f"{Fore.RESET}Waiting for downloads...")

    for future in work:
        print(f"{Fore.CYAN}{future.result()}")

    print(f"{Fore.RESET}Done")


if __name__ == "__main__":
    main(mode="process")
    # main(mode="thread")
