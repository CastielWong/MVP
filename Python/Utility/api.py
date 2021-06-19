#!/usr/bin/env python
# -*- coding: utf-8 -*-
from requests import Request, Session
import requests


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

    print(response.status_code)
    print(response.text)

    return


def retrieve_oauth_link(redirect_url: str, client_id: str) -> str:
    """Retrieve the OAuth link.
    Reference: https://realpython.com/python-api/

    Args:
        redirect_url: the Authorization callback URL
        client_id: client ID of the URL

    Returns:
        The URL used for OAuth
    """
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_url,
        "scope": "user",
        "response_type": "code",
    }

    endpoint = "https://github.com/login/oauth/authorize"
    response = requests.get(endpoint, params=params)
    url = response.url
    return url
