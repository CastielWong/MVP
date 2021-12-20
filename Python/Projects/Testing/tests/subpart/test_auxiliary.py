#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test the auxiliary module."""
from typing import Dict, TypeVar
import sys

from pytest_mock import MockerFixture
from requests import Response
from conftest import _PATH_PACKAGE
import pytest

# in case path not located
sys.path.append(_PATH_PACKAGE)
# pylint: disable=C0413(wrong-import-position)
from core.subpart import auxiliary  # noqa: E402

ResourceS3 = TypeVar("ResourceS3")


_MOCKING_CONTENT = {
    "success": {"url": "https://httpbin.org/anything", "code": 200},
    "failure": {"url": "https://httpbin.org/nothing", "code": 404},
}


def test_get_url_mock(mocker: MockerFixture, mock_config_conn: Dict[str, Dict]):
    """Verify the mocking of URL.

    Args:
        mocker: fixture used to mock
        mock_config_conn: connection acquired from the root conftest
    """
    expected_url = "https://mocking_test"
    expected_content = "It's mocking content"

    def mock_session_get(self, url: str) -> Response:
        # pylint: disable=W0212(protected-access)
        # pylint: disable=W0613(unused-argument)
        print(f"Mocking get for URL: {url}")
        response = Response()
        response.status_code = 200
        response.url = expected_url
        response._content = expected_content

        return response

    mocker.patch("requests.Session.get", mock_session_get)
    res = auxiliary.get_url(url=mock_config_conn["remote"])

    assert res.status_code == 200
    assert res.url == expected_url
    assert res.content == expected_content

    return


@pytest.mark.parametrize("response", ["success", "failure"])
def test_get_url_actual(response: str):
    """Verify the mocking of URL.

    Args:
        response: expected response from the url
    """
    res = auxiliary.get_url(url=_MOCKING_CONTENT[response]["url"])

    assert res.status_code == _MOCKING_CONTENT[response]["code"]
    assert res.url == _MOCKING_CONTENT[response]["url"]

    return
