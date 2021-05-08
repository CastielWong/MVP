#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests import Response, Session


def get_url(url) -> Response:
    session = Session()

    with session as s:
        response = s.get(url)

    return response
