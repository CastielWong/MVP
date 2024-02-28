#!/usr/bin/env -S python -m pytest
# -*- coding: utf-8 -*-
"""Test for FTP connection."""
# pylint: disable=W0212 (protected-access)
from ftplib import FTP  # nosec
from typing import Optional
import os
import shutil

from paramiko import SSHClient
from pyfakefs.fake_filesystem import FakeFilesystem
from pytest_mock import MockerFixture
import pytest

from src.connection.ftp import FTPClient, SecureFTPClient

_DUMMY_REMOTE = "/dummy/remote"
_DUMMY_LOCAL = "dummy/local"
_DUMMY_CSV = "ham.csv"

_CSV_TO_DOWNLOAD = os.path.join(_DUMMY_REMOTE, _DUMMY_CSV)

DUMMY_HOST = "dummy_host"
DUMMY_USERNAME = "dummy_user"
DUMMY_PASSWORD = "dummy_pass"  # noqa: S105 (hardcoded-password-string)
DUMMY_TIMEOUT = 180

DUMMY_FTP = FTPClient(
    host=DUMMY_HOST,
    username=DUMMY_USERNAME,
    password=DUMMY_PASSWORD,
    timeout=DUMMY_TIMEOUT,
)
DUMMY_SFTP = SecureFTPClient(
    host=DUMMY_HOST,
    username=DUMMY_USERNAME,
    password=DUMMY_PASSWORD,
    timeout=DUMMY_TIMEOUT,
)


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


# -------------------------------------------------------------------------------------
# FTP
# -------------------------------------------------------------------------------------
def test_ftp__check_connection_open(mocker: MockerFixture):
    """Verify the FTP connection."""
    patcher_connect = mocker.patch("ftplib.FTP.connect", return_value=None)
    patcher_login = mocker.patch("ftplib.FTP.login", return_value=None)

    with DUMMY_FTP:
        patcher_connect.assert_called_with(
            host=DUMMY_HOST,
            port=21,
            timeout=DUMMY_TIMEOUT,
        )
        patcher_login.assert_called_with(user=DUMMY_USERNAME, passwd=DUMMY_PASSWORD)
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
    # mute the actual downloading
    mocker.patch("ftplib.FTP.retrbinary", return_value=None)

    fs.create_file(
        file_path=_CSV_TO_DOWNLOAD, contents="for 'test_ftp__download_file()'"
    )

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


# -------------------------------------------------------------------------------------
# SFTP
# -------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "password, key_file",
    [
        (None, ""),
        ("", None),
        ("", ""),
        (None, None),
    ],
)
def test_sftp__initialization_exception__neither(
    password: Optional[str], key_file: Optional[str]
):
    """Check when the initialization has neither password nor cert."""
    with pytest.raises(ValueError) as exc_info:
        SecureFTPClient(host=DUMMY_HOST, password=password, key_file=key_file)
        assert (
            exc_info.value
            == "Please provide either password or the key file for authentication."
        )
    return


def test_sftp__initialization_exception__both():
    """Check when the initialization has both password and cert."""
    with pytest.raises(NotImplementedError) as exc_info:
        SecureFTPClient(
            host=DUMMY_HOST,
            password="a_password",  # noqa: S106 (hardcoded-password-func-arg)
            key_file="a_key.pem",
        )
        assert (
            exc_info.value
            == "Please provide either password or the key file, but not both."
        )
    return


def test_sftp__check_connection_open(mocker: MockerFixture):
    """Verify the SFTP connection."""
    mocker.patch("paramiko.SSHClient.open_sftp", return_value=SSHClient())
    patcher = mocker.patch("paramiko.SSHClient.connect", return_value=None)

    with DUMMY_SFTP:
        patcher.assert_called_with(
            host=DUMMY_HOST,
            port=22,
            username=DUMMY_USERNAME,
            password=DUMMY_PASSWORD,
            pkey=None,
            timeout=DUMMY_TIMEOUT,
            disabled_algorithms={"pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]},
        )
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


def test_sftp__download_file(mocker: MockerFixture, fs: FakeFilesystem):
    """Verify file downloaded in SFTP."""
    # create directories for file manipulation
    for dir_name in (_DUMMY_REMOTE, _DUMMY_LOCAL):
        fs.create_dir(dir_name)

    expected_path = os.path.join(_DUMMY_LOCAL, _DUMMY_CSV)

    def mock_download(**kwargs):  # pylint: disable=W0613 (unused-argument)
        fs.create_file(
            file_path=_CSV_TO_DOWNLOAD, contents="for 'test_sftp__download_file'"
        )
        shutil.copy(_CSV_TO_DOWNLOAD, expected_path)
        return

    DUMMY_SFTP.exists_file = mocker.MagicMock(return_value=True)  # type: ignore
    # check = mocker.patch("paramiko.SFTPClient.get", side_effect=mock_download)
    mocker.patch.object(DUMMY_SFTP._client, "get", side_effect=mock_download)

    # check the file is not "downloaded" before the operation
    assert fs.exists(expected_path) is False

    result = DUMMY_SFTP.download_file(_CSV_TO_DOWNLOAD, _DUMMY_LOCAL)

    # confirm such file is "downloaded" after
    assert result is True
    assert fs.exists(expected_path) is True
    DUMMY_SFTP.exists_file.assert_called_once_with(_CSV_TO_DOWNLOAD)  # type: ignore
    DUMMY_SFTP._client.get.assert_called_once_with(  # type: ignore
        remotepath=_CSV_TO_DOWNLOAD, localpath=expected_path
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
