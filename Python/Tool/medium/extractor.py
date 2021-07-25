#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Dict
import re

START_FACTOR = 0
START_FACTOR = 1
START_FACTOR = 2
START_FACTOR = 3
START_FACTOR = 4
START_FACTOR = 5
# START_FACTOR = 6


MULTIPLIER = 4
START_INDEX = START_FACTOR * MULTIPLIER


def extract_post(text: str) -> str:
    # pattern_v1 = r"\((https://medium\.com/(.)+)\?source=3D[=]?email.+\&sectionName=3D.+\)"    # noqa: E501
    pattern = r"<a href=3D\"(https://medium\.com/[^?]+)\?source=3Demail.+none;\">"
    matcher = re.search(pattern, text, re.IGNORECASE)

    # return an empty string if there is no match
    if not matcher:
        return ""

    # get the second group for the post
    return matcher.group(1)


def retrieve_posts(source: str) -> Dict[str, int]:
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
    import subprocess

    commands = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "--args",
        "--incognito",
        url,
    ]

    subprocess.run(commands)


def main():
    source = "source.txt"
    # source = "previous.txt"

    posts = retrieve_posts(source)

    counter = 0
    for post, index in posts.items():
        # start from the index indicated
        if index < START_INDEX:
            continue

        # stop when the limit is reached
        if counter == MULTIPLIER:
            break

        print(f"{index}:\t{post}")
        open_link_in_chrome_incognito(post)
        counter += 1


if __name__ == "__main__":
    main()
