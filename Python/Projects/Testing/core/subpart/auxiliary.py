#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Auxiliary component."""
from typing import List

from requests import Response, Session


def get_url(url: str) -> Response:
    """Get the response from the URL.

    Args:
        url: URL to send the get request

    Returns:
        The response returned from URL
    """
    session = Session()

    with session as sess:
        response = sess.get(url)

    return response


def get_content_in_range(file_name: str, start: int, end: int) -> List[str]:
    """Retrieve file content at the range specified.

    Args:
        file_name: file to retrieve contents
        start: start line number
        end: end line number

    Returns:
        List of lines
    """
    results = []

    counter = 0

    with open(file_name, "r") as f_r:
        line = " "

        while line:
            counter += 1
            line = f_r.readline()

            if counter < start:
                continue

            results.append(line)

            if counter >= end:
                break

    return results
