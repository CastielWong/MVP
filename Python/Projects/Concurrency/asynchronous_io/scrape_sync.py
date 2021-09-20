#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Demo to process web scrping synchronously."""
from datetime import datetime

from colorama import Fore
import bs4
import requests


def get_html(episode_number: int) -> str:
    """Get html of the corresponding episode number.

    Args:
        episode_number: the episode number

    Returns:
        Text in HTML
    """
    print(f"{Fore.YELLOW}Getting HTML for episode {episode_number}")

    url = f"https://talkpython.fm/{episode_number}"
    res = requests.get(url)
    res.raise_for_status()

    return res.text


def get_title(html: str, episode_number: int) -> str:
    """Get title of the corresponding episode number.

    Args:
        html: content of html page
        episode_number: the episode number

    Returns:
        Title of the episode
    """
    print(f"{Fore.CYAN}Getting TITLE for episode {episode_number}")

    soup = bs4.BeautifulSoup(html, "html.parser")
    header = soup.select_one("h1")

    if not header:
        return "MISSING"

    return header.text.strip()


def get_title_range() -> None:
    """Get titles of the specified range one by one."""
    for e_n in range(150, 160):
        html = get_html(e_n)
        title = get_title(html, e_n)

        print(f"{Fore.WHITE}Title found: {title}")

    return


def main() -> None:
    """Execute the main workflow."""
    t0 = datetime.now()

    get_title_range()
    elapsed = datetime.now() - t0

    print(f"Done in {elapsed.total_seconds():.2f} seconds.")

    return


if __name__ == "__main__":
    main()
