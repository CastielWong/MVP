#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
import requests
from requests import Request, Session


def get_result_via_json(
    base_url: str, endpoint: str, file_name: str, api_token: str, expected: str
) -> None:
    """Retrieve expected result via API from JSON input.

    Args:
        base_url: the base URL
        endpoint: endpoint of the request API
        file_name: name of the JSON file
        api_token: API token applied
        expected: the expected portion of the response in JSON
    """
    response = requests.get(
        f"{base_url}/{endpoint}/{file_name}.json?api-key={api_token}"
    )
    results = response.json()["{expected}"]

    for item in results:
        print(item)
    return


def wrap_up_api(url: str, username: str, password: str) -> None:
    """Wrap up the API to get the response.

    Args:
        url: URL of the API
        username: the needed user name
        password: the needed password
    """
    HEADERS = {
        "Content-Type": "application.json",
        "Accept": "application/json",
    }
    req = Request("Get", url={url}, headers=HEADERS, auth=({username}, {password}))
    prepped = req.prepare()

    with Session as s:
        response = s.send(prepped)

    print(response.text)
    print(response.content)

    return
