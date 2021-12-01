#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Extract url links from Medium marketing email text."""
from argparse import ArgumentParser
from typing import Dict
import re
import subprocess  # nosec

MULTIPLIER = 4  # define how many pages open at a time


def create_parser() -> ArgumentParser:
    """Create the parser."""
    parser = ArgumentParser(
        description=(
            "Extract Medium links automatically then access through Google Chrome "
            '"Incognito" mode'
        )
    )
    parser.add_argument(
        "--source", type=str, default="source.txt", help="specify the raw source file"
    )

    mandatory = parser.add_argument_group("mandatory arguments")
    mandatory.add_argument(
        "-f",
        "--factor",
        required=True,
        type=int,
        default=0,
        help="set the factor to the start index",
    )

    return parser


def extract_post(text: str) -> str:
    """Extract post from the text.

    Args:
        text: raw text from Medium

    Returns:
        HTTPS link extracted
    """
    # pattern_v1 = r"\((https://medium\.com/(.)+)\?source=3D[=]?email.+\&sectionName=3D.+\)"    # noqa: E501
    pattern = r"<a href=3D\"(https://medium\.com/[^?]+)\?source=3Demail.+none;\">"
    matcher = re.search(pattern, text, re.IGNORECASE)

    # return an empty string if there is no match
    if not matcher:
        return ""

    # get the second group for the post
    return matcher.group(1)


def retrieve_posts(source: str) -> Dict[str, int]:
    """Retrieve posts from Medium raw text.

    Args:
        source: the raw source text

    Returns:
        Dictionary mapping from web link to index number
    """
    mapping = {}

    counter = 0
    current_row = ""
    with open(source, "r") as file_reader:
        line = file_reader.readline()

        while line:
            # remove the trailing newline
            if len(line) > 1 and line[-1] == "\n":
                line = line.strip()
                # remove the trailing "=" for line
                if line[-1] == "=":
                    line = line[:-1]
            # reset current row after previous truncated line is processed
            if "<a" in line:
                post = extract_post(current_row)
                # add the post if
                if (
                    # not empty
                    post
                    # not an author or function page
                    and post.count("/") > 3
                    # not duplicate
                    and post not in mapping
                ):
                    mapping[post] = counter
                    counter += 1

                # reset current row
                current_row = ""

            # concatenate separate lines together
            current_row += line

            line = file_reader.readline()

    return mapping


def open_link_in_chrome_incognito(url: str) -> None:
    """Open the link via Incognito mode in Google Chrome.

    Args:
        url: the url link to access
    """
    commands = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--args",
        "--incognito",
        url,
    ]

    subprocess.check_output(commands)  # nosec

    return


def main(source: str, factor: int) -> None:
    """Execute as the entry point.

    Args:
        source: file path which stores raw text acquired from Medium marketing email
        factor: factor used to calculate the start index
    """
    start_index = factor * MULTIPLIER

    posts = retrieve_posts(source)

    counter = 0
    for post, index in posts.items():
        # start from the index indicated
        if index < start_index:
            continue

        # stop when the limit is reached
        if counter == MULTIPLIER:
            break

        print(f"{index}:\t{post}")
        open_link_in_chrome_incognito(post)
        counter += 1

    return


if __name__ == "__main__":
    args_parser = create_parser()
    args = args_parser.parse_args()

    main(source=args.source, factor=args.factor)
