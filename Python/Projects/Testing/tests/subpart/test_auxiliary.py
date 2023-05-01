#!/usr/bin/env -S pytest
# -*- coding: utf-8 -*-
"""Test the auxiliary module."""
from typing import Dict, List, TypeVar
import sys

from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture
from requests import Response
from conftest import _PATH_PACKAGE
import pytest

# in case path not located
sys.path.append(_PATH_PACKAGE)
# pylint: disable=C0413(wrong-import-position)
from core.subpart import auxiliary  # noqa: E402

ResourceS3 = TypeVar("ResourceS3")

_FILE_LINES = [f"0{x}" if x < 10 else str(x) for x in range(1, 21)]

_MOCKING_CONTENT = {
    "success": {"url": "https://httpbin.org/anything", "code": 200},
    "failure": {"url": "https://httpbin.org/nothing", "code": 404},
}


def test_get_content_in_range(mocker: MockerFixture):
    """Verify content retrieving is functioning well.

    Args:
        mocker: fixture used to mock
    """
    mock_file = mocker.mock_open(read_data="\n".join(_FILE_LINES))
    mocker.patch(target="core.subpart.auxiliary.open", new=mock_file)

    results = auxiliary.get_content_in_range(
        file_name="dummy",
        start=2,
        end=10,
    )

    assert len(results) == 9
    assert results[0].strip() == "02"
    assert results[-1].strip() == "10"

    return


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

    mocker.patch(target="requests.Session.get", new=mock_session_get)
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


@pytest.mark.parametrize(
    "real_number, expected",
    [
        # general case
        (2, "2"),
        (1.2, "1.2"),
        (1.201, "1.201"),
        # decimal point
        (2.0, "2"),
        (1.20, "1.2"),
        (1.200_000, "1.2"),
        (1.200_000_00, "1.2"),
        (0.3, "0.3"),
        # scientific notation
        (1.0e3, "1000"),
        (1.0e16, "10000000000000000"),
        (1.001e16, "10010000000000000"),
        (1.0e-3, "0.001"),
        (8.123_456_789_123_45e-05, "0.0000812345678912345"),
        (8.123_456_789_123_45e-06, "0.00000812345678912345"),
        (8.123_456_789_123_45e-09, "0.00000000812345678912345"),
    ],
)
def test_format_float_with_precision(real_number, expected):
    """Verify the float to string type formatting.

    Args:
        real_number: input float number
        expected: expected string outputted
    """
    check = auxiliary.format_float_with_precision(real_number)

    assert check == expected

    return


@pytest.mark.parametrize(
    "data_in_csv, data_in_yaml",
    [
        (["a", "1"], ["- a: 1"]),
        (
            [
                "a,b,c",
                "1,one,alpha",
                "2,two,beta",
            ],
            [
                "- a: 1",
                "  b: one",
                "  c: alpha",
                "- a: 2",
                "  b: two",
                "  c: beta",
            ],
        ),
        (
            [
                "a,b,c",
                "1,,alpha",
                "2,two,",
            ],
            [
                "- a: 1",
                "  b: .nan",
                "  c: alpha",
                "- a: 2",
                "  b: two",
                "  c: .nan",
            ],
        ),
    ],
)
def test_convert_csv_to_yaml(
    fs: FakeFilesystem, data_in_csv: List[str], data_in_yaml: List[str]
):
    """Verify the functionality to convert CSV file to YAML.

    Args:
        fs: fake file system to manipulate IO
        data_in_csv: list of data in csv format
        data_in_yaml: list of data in yaml format
    """
    file_name = "dummy"
    fs.create_file(f"{file_name}.csv", contents="\n".join(data_in_csv))

    auxiliary.convert_csv_to_yaml(f"{file_name}.csv")

    with open(f"{file_name}.yaml", "r", encoding="utf-8") as f_r:
        contents = f_r.readlines()

    assert "".join(contents).strip() == "\n".join(data_in_yaml)

    return
