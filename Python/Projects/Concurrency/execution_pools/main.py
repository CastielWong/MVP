#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demonstrate how to easily swop between multithreading and multiprocessing."""
from concurrent.futures import Future
from concurrent.futures.process import ProcessPoolExecutor as PoolExecutor
import multiprocessing

import requests
import bs4

# from concurrent.futures.thread import ThreadPoolExecutor as PoolExecutor


def get_title(url: str) -> str:
    """Get html of the corresponding episode number.

    Args:
        episode_number: the episode number

    Returns:
        Text in HTML
    """
    process = multiprocessing.current_process()
    print(
        f"Getting title from {url.replace('https://', '')}, "
        f"PID: {process.pid}, ProcName: {process.name}",
        flush=True,
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

    if not tag:
        return "NONE"

    if not tag.text:
        anchor = tag.select_one("a")
        if anchor and anchor.text:
            return anchor.text

        if anchor and "title" in anchor.attrs:
            return anchor.attrs["title"]

        return "NONE"

    return tag.get_text(strip=True)


def main() -> None:
    """Execute the main workflow."""
    urls = [
        "https://talkpython.fm",
        "https://pythonbytes.fm",
        "https://google.com",
        "https://realpython.com",
        "https://training.talkpython.fm/",
    ]

    work = []

    with PoolExecutor() as executor:
        for url in urls:
            # print(
            #     f"Getting title from {url.replace('https', '')}",
            #     end='... ',
            #     flush=True,
            # )
            # title = get_title(url)
            future: Future = executor.submit(get_title, url)
            work.append(future)

        print("Waiting for downloads...", flush=True)

    print("Done", flush=True)
    for future in work:
        print(f"{future.result()}", flush=True)


if __name__ == "__main__":
    main()
