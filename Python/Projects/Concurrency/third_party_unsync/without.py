#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demo a program running without any asynchronous technologies."""
from datetime import datetime
import math
import time

from colorama import Fore
from colorama.ansi import AnsiFore
import requests


def compute_some() -> None:
    """Perform computing intensive operation."""
    print(f"{Fore.YELLOW}Computing...")

    for _ in range(1, 10_000_000):
        math.sqrt(25 ** 25 + 0.01)

    return


def download_some(url: str, msg: str = "", color: AnsiFore = Fore.BLUE) -> None:
    """Perform network intensive operation.

    Args:
        url: url to download
        msg: message to print
        color: color to print
    """
    if not msg:
        msg = "Downloading..."
    print(f"{color}{msg}")

    resp = requests.get(url)
    resp.raise_for_status()

    text = resp.text

    print(f"{color}Length of characters downloaded: {len(text):,}.")

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
        download_some(
            url="https://talkpython.fm/episodes/show/102/effective-code-reviews",
        )

    for _ in range(2):
        download_some(
            url="https://pythonbytes.fm/episodes/show/92/will-your-python-be-compiled",
            msg="Downloading more....",
            color=Fore.LIGHTBLUE_EX,
        )

    for _ in range(4):
        wait_some()

    elapsed = datetime.now() - t0
    print(
        f"{Fore.RESET}"
        f"Synchronous version done in {elapsed.total_seconds():,.2f} seconds."
    )

    return


if __name__ == "__main__":
    main()
