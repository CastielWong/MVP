#!/usr/bin/env -S python -m pytest
# -*- coding: utf-8 -*-
"""Test for FTP connection."""
from ftplib import FTP  # nosec
import os

from pyfakefs.fake_filesystem import FakeFilesystem
from paramiko import SSHClient
from pytest_mock import MockerFixture
from core.ftp import FTPClient, SecureFTPClient
import pytest

_DUMMY_REMOTE = "/dummy/remote"
_DUMMY_LOCAL = "dummy/local"
_DUMMY_CSV = "ham.csv"


_CSV_TO_DOWNLOAD = os.path.join(_DUMMY_REMOTE, _DUMMY_CSV)


ftp_config = {
    "hostname": "dummy_host",
    "username": "dummy_user",
    "password": "dummy_pass",
}
DUMMY_FTP = FTPClient(**ftp_config, port=21)
DUMMY_SFTP = SecureFTPClient(**ftp_config, port=22)


@pytest.mark.parametrize("client", [DUMMY_FTP, DUMMY_SFTP])
def test_check_connection_open__none(client: FTPClient):
    """Verify exception raised when there is no connection."""
    client._client = None
    with pytest.raises(Exception) as exc_info:
        client.check_connection_open()

    assert str(exc_info.value) == (
        "Connection of SFTP is wrapped as context manager, "
        "please use `with` to open a connection."
    )
    return


def test_ftp__check_connection_open(mocker: MockerFixture):
    """Verify the FTP connection."""
    mocker.patch("ftplib.FTP.connect", return_value=None)
    mocker.patch("ftplib.FTP.login", return_value=None)

    with DUMMY_FTP:
        assert isinstance(DUMMY_FTP._client, FTP)
    return


def test_ftp__exists_file(mocker: MockerFixture):
    """Verify when there is a file exists in FTP connection."""
    DUMMY_FTP._client = mocker.MagicMock()
    mocker.patch("ftplib.FTP.nlst", return_value=[_CSV_TO_DOWNLOAD])

    result = DUMMY_FTP.exists_file(_CSV_TO_DOWNLOAD)

    assert result is True
    return


def test_ftp__download_file(mocker: MockerFixture, fs: FakeFilesystem):
    """Verify file is downloaded in FTP."""
    DUMMY_FTP._client = mocker.MagicMock()
    mocker.patch("ftplib.FTP.pwd", return_value=None)
    mocker.patch("ftplib.FTP.cwd", return_value=None)
    mocker.patch("ftplib.FTP.retrbinary", return_value=None)

    fs.create_file(file_path=_CSV_TO_DOWNLOAD, contents="")

    DUMMY_FTP._client.nlst = mocker.MagicMock(  # type: ignore
        return_value=[_CSV_TO_DOWNLOAD]
    )

    result = DUMMY_FTP.download_file(_CSV_TO_DOWNLOAD, _DUMMY_LOCAL)

    assert result is True
    return


def test_ftp__download_file__nonexistent(mocker: MockerFixture):
    """Verify when there is no such file to download in FTP."""
    DUMMY_FTP._client = mocker.MagicMock()
    mocker.patch("ftplib.FTP.pwd", return_value=None)
    mocker.patch("ftplib.FTP.cwd", return_value=None)

    DUMMY_FTP._client.nlst = mocker.MagicMock(  # type: ignore
        return_value=["/dummy/remote/ham", "/dummy/remote/spam"]
    )

    result = DUMMY_FTP.download_file(_CSV_TO_DOWNLOAD, _DUMMY_LOCAL)

    assert result is False
    return


def test_sftp__check_connection_open(mocker: MockerFixture):
    """Verify the SFTP connection."""
    mocker.patch("paramiko.SSHClient.connect", return_value=None)
    mocker.patch("paramiko.SSHClient.open_sftp", return_value=SSHClient())

    with DUMMY_SFTP:
        assert isinstance(DUMMY_SFTP._client, SSHClient)
    return


def test_sftp__exists_file(mocker: MockerFixture):
    """Verify when there is a file exists in SFTP connection."""
    DUMMY_SFTP._client = mocker.MagicMock()
    DUMMY_SFTP._client.stat.return_value = "dummy_stat"  # type: ignore
    result = DUMMY_SFTP.exists_file(_CSV_TO_DOWNLOAD)

    assert result is True
    DUMMY_SFTP._client.stat.assert_called_once_with(_CSV_TO_DOWNLOAD)  # type: ignore
    return


def test_sftp__exists_file__nonexistent(mocker: MockerFixture):
    """Verify when there is no file exists in SFTP."""
    DUMMY_SFTP._client = mocker.MagicMock()
    DUMMY_SFTP._client.stat.side_effect = IOError()  # type: ignore
    result = DUMMY_SFTP.exists_file(_CSV_TO_DOWNLOAD)

    assert result is False
    DUMMY_SFTP._client.stat.assert_called_once_with(_CSV_TO_DOWNLOAD)  # type: ignore
    return


def test_sftp__download_file(mocker: MockerFixture):
    """Verify file downloaded in SFTP."""
    DUMMY_SFTP._client.get = mocker.MagicMock()  # type: ignore
    DUMMY_SFTP.exists_file = mocker.MagicMock(return_value=True)  # type: ignore

    result = DUMMY_SFTP.download_file(_CSV_TO_DOWNLOAD, _DUMMY_LOCAL)

    assert result is True
    DUMMY_SFTP.exists_file.assert_called_once_with(_CSV_TO_DOWNLOAD)  # type: ignore
    DUMMY_SFTP._client.get.assert_called_once_with(  # type: ignore
        remotepath=_CSV_TO_DOWNLOAD, localpath=os.path.join(_DUMMY_LOCAL, _DUMMY_CSV)
    )
    return


def test_sftp__download_file__nonexistent(mocker: MockerFixture):
    """Verify when there is no such file to download in SFTP."""
    DUMMY_SFTP._client.get = mocker.MagicMock()  # type: ignore
    DUMMY_SFTP.exists_file = mocker.MagicMock(return_value=False)  # type: ignore

    result = DUMMY_SFTP.download_file(_CSV_TO_DOWNLOAD, _DUMMY_LOCAL)

    assert result is False
    DUMMY_SFTP.exists_file.assert_called_once_with(_CSV_TO_DOWNLOAD)  # type: ignore
    DUMMY_SFTP._client.get.assert_not_called()  # type: ignore
    return
