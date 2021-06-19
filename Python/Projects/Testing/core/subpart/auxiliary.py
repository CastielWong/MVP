#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests import Response, Session


def get_url(url: str) -> Response:
    """Get the response from the URL.

    Args:
        url: URL to send the get request

    Returns:
        The response returned from URL
    """
    session = Session()

    with session as s:
        response = s.get(url)

    return response
