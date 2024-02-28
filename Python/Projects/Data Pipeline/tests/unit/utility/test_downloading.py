# -*- coding: utf-8 -*-
"""Test download."""
from pathlib import Path
import gzip
import os

from pytest_mock import MockerFixture
import pytest
import requests

from src.utility import downloading

DUMMY_NFS_LOCATION = "tmp_nfs"


def test_download_from_ftp(mocker: MockerFixture, monkeypatch):
    """Verify the download."""
    monkeypatch.setenv("DUMMY_FTP_PASSWORD", "nothing1$real")

    source_file = "/storage/20231005/infix/dummy.csv"
    dir_target = "/opt/vendor/"

    # prepare for SecureFTPClient mocking
    check = mocker.MagicMock()

    mocker.patch("paramiko.SSHClient", mocker.MagicMock())
    mocker.patch("src.connection.ftp.SecureFTPClient.__enter__", return_value=check)
    mocker.patch(
        "src.connection.ftp.SecureFTPClient.__exit__",
        return_value=mocker.MagicMock(),
    )

    downloading.download_from_ftp(source_file=source_file, dir_target=dir_target)

    # verify the `SecureFTPClient.download_file()` is called with expected parameters
    check.download_file.assert_called_with(ftp_path=source_file, dir_local=dir_target)

    return


@pytest.mark.parametrize(
    "content_type, content_encoding, file_path, expected_file_path, should_warn",
    [
        # normal use case
        pytest.param("text/csv", "", "dir/file.csv", "dir/file.csv", False),
        # no content type or content encoding
        pytest.param("", "", "dir/file", "dir/file", False),
        # should warn when header extension doesn't match provided
        pytest.param("application/pdf", "", "dir/file.csv", "dir/file.csv", True),
        # should warn when header extension is not compressed but the provided extension
        # is compressed
        pytest.param("text/csv", "", "dir/file.csv.gz", "dir/file.csv.gz", True),
        # should append compression extension
        pytest.param("application/gzip", "", "dir/file.csv", "dir/file.csv.gz", False),
        # shouldn't append compression extension if file path already contains it
        pytest.param(
            "application/gzip", "", "dir/file.csv.gz", "dir/file.csv.gz", False
        ),
        # should append all content encodings to file path
        pytest.param(
            "text/csv", "gzip, br", "dir/file.csv", "dir/file.csv.gz.br", False
        ),
        # shouldn't append all content encodings to file path if file path already
        # contains it
        pytest.param(
            "text/csv", "gzip, br", "dir/file.csv.gz.br", "dir/file.csv.gz.br", False
        ),
    ],
)
def test_download_raw_response(
    requests_mock,
    caplog,
    content_type,
    content_encoding,
    file_path,
    expected_file_path,
    should_warn,
):
    """Summary.

    Args:
        requests_mock: _description_
        caplog: _description_
        content_type: _description_
        content_encoding: _description_
        file_path: _description_
        expected_file_path: _description_
        should_warn: _description_
    """
    table_path = f"{DUMMY_NFS_LOCATION}/table_name"
    file_path = os.path.join(table_path, file_path)
    expected_file_path = os.path.join(table_path, expected_file_path)

    write_bytes = b"data"
    if content_encoding:
        write_bytes = gzip.compress(write_bytes)

    requests_mock.get(
        "https://mock_url",
        content=write_bytes,
        headers={"Content-Type": content_type, "Content-Encoding": content_encoding},
    )
    resp = requests.get("https://mock_url", stream=True, timeout=30)
    actual_file_path = downloading.download_raw_response(
        resp,
        file_path,
        is_stream=True,
        overwrite=True,
    )

    log_levels = [record.levelname for record in caplog.records]
    if should_warn:
        assert "WARNING" in log_levels
    else:
        assert "WARNING" not in log_levels

    assert expected_file_path == actual_file_path
    with open(actual_file_path, mode="rb") as fp:
        read_bytes = fp.read()
    assert read_bytes == write_bytes

    return


@pytest.mark.parametrize(
    "stream, content_encoding, exception",
    [
        (True, "", None),
        (False, "", None),
        (True, "gzip", None),
        (False, "gzip", ValueError),
    ],
)
def test_download_raw_response_stream(
    requests_mock, stream: bool, content_encoding: str, exception: Exception
):
    """Summary.

    Args:
        requests_mock: _description_
        stream: _description_
        content_encoding: _description_
        exception: _description_
    """
    file_path = os.path.join(f"{DUMMY_NFS_LOCATION}/table_name", "file")
    write_bytes = b"data"
    if content_encoding:
        write_bytes = gzip.compress(write_bytes)

    requests_mock.get(
        "https://mock_url",
        content=write_bytes,
        headers={"Content-Encoding": content_encoding},
    )
    resp = requests.get("https://mock_url", stream=stream, timeout=30)

    if exception:
        with pytest.raises(exception):
            downloading.download_raw_response(
                resp, file_path, is_stream=stream, overwrite=True
            )
    else:
        file_path = downloading.download_raw_response(
            resp,
            file_path,
            is_stream=stream,
            overwrite=True,
        )
        with open(file_path, mode="rb") as fp:
            read_bytes = fp.read()
        assert read_bytes == write_bytes

    return


@pytest.mark.parametrize(
    "file_name, overwrite, exception",
    [("file1", True, None), ("file2", False, FileExistsError)],
)
def test_download_raw_response_overwrite(
    requests_mock,
    file_name: str,
    overwrite: bool,
    exception: Exception,
):
    """Summary.

    Args:
        requests_mock: _description_
        file_name: _description_
        overwrite: _description_
        exception: _description_
    """
    file_path = os.path.join(f"{DUMMY_NFS_LOCATION}/table_name", "file")
    Path(file_path).parent.mkdir(parents=True, exist_ok=True)

    write_bytes = b"data"
    with open(file_path, mode="wb") as fp:
        fp.write(write_bytes)

    requests_mock.get(
        "https://mock_url",
        content=write_bytes,
    )
    resp = requests.get("https://mock_url", timeout=30)

    if exception:
        with pytest.raises(exception):
            downloading.download_raw_response(resp, file_path, overwrite=overwrite)
    else:
        downloading.download_raw_response(resp, file_path, overwrite=overwrite)

    return
