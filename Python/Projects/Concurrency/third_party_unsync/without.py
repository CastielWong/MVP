#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demo a program running without any asynchronous technologies."""
from datetime import datetime
import math
import time

from colorama import Fore
import requests


def compute_some() -> None:
    """Perform computing intensive operation."""
    print(f"{Fore.YELLOW}Computing...")

    for _ in range(1, 10_000_000):
        math.sqrt(25 ** 25 + 0.01)

    return


def download_some() -> None:
    """Perform network intensive operation."""
    print(f"{Fore.BLUE}Downloading...")

    url = (
        "https://talkpython.fm/episodes/show/174/"
        "coming-into-python-from-another-industry-part-2"
    )
    resp = requests.get(url)
    resp.raise_for_status()

    text = resp.text

    print(f"Downloaded (more) {len(text):,} characters.")

    return


def download_some_more() -> None:
    """Perform more network intensive operation."""
    print(f"{Fore.LIGHTBLUE_EX}Downloading more ...")

    url = "https://pythonbytes.fm/episodes/show/92/will-your-python-be-compiled"
    resp = requests.get(url)
    resp.raise_for_status()

    text = resp.text

    print(f"Downloaded {len(text):,} characters.")

    return


def wait_some() -> None:
    """Simulate IO intensive operation."""
    print(f"{Fore.GREEN}Waiting...")

    for _ in range(1, 1_000):
        time.sleep(0.001)

    return


def main() -> None:
    """Execute the main workflow."""
    t0 = datetime.now()

    for _ in range(3):
        compute_some()

    for _ in range(2):
        download_some()

    for _ in range(2):
        download_some_more()

    for _ in range(4):
        wait_some()

    dt = datetime.now() - t0
    print(f"{Fore.RESET}Synchronous version done in {dt.total_seconds():,.2f} seconds.")

    return


if __name__ == "__main__":
    main()
