#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from typing import Dict

from pytest_mock import MockerFixture
from requests import Response

from conftest import _PATH_PACKAGE

# in case path not located
sys.path.append(_PATH_PACKAGE)
from core.subpart import auxiliary  # noqa: E402


_MOCKING_CONTENT = {
    200: "The page can be accessed normally",
    404: "There is no such page",
}


def test_get_url(mocker: MockerFixture, mock_config_conn: Dict[str, Dict]):
    def mock_session_get(self, url: str) -> Response:
        response = Response()
        response.status_code = 200
        response.utl = "https://mocking_test"
        response._content = _MOCKING_CONTENT[200]

        return response

    mocker.patch("requests.Session.get", mock_session_get)
    res = auxiliary.get_url(url=mock_config_conn["remote"])

    assert res.status_code == 200
    assert res.utl == "https://mocking_test"
    assert res.content == _MOCKING_CONTENT[200]

    return
